"""
This module contains a number of globals, which are set by the execution when its
processing nodes. 

They are used as a side channel to pass values from the executor to special functions
which need to know more about the execution context, like in the `exec` to know
the source code of the current node.

This module exposes three global functions, which are meant to be used like:

1. The `executor` calls `set_context` before executing every call node.
2. The function being called can call `get_context` to get the current context.
3. The `executor` calls `teardown_context` after its finished executing
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, Iterable, List, Mapping, Optional

from lineapy.execution.globals_dict import GlobalsDict, GlobalsDictResult
from lineapy.execution.inspect_function import is_mutable
from lineapy.execution.side_effects import (
    ID,
    AccessedGlobals,
    ExecutorPointer,
    MutatedNode,
    SideEffect,
    SideEffects,
    Variable,
    ViewOfNodes,
)

if TYPE_CHECKING:
    from lineapy.data.types import CallNode, LineaID
    from lineapy.execution.executor import Executor

_global_variables: GlobalsDict = GlobalsDict()
_current_context: Optional[ExecutionContext] = None


@dataclass
class ExecutionContext:
    """
    The context available to call nodes during an execution
    """

    # The current node being executed
    node: CallNode
    # The executor that is running
    executor: Executor

    # Mapping from each input global name to its ID
    _input_node_ids: Mapping[str, LineaID]
    # Mapping from each input global name to whether it is mutable
    _input_globals_mutable: Mapping[str, bool]

    # Additional side effects triggered during this executiong.
    # The exec function will add to this and we will retrieve it at the end.
    side_effects: List[SideEffect] = field(default_factory=list)

    @property
    def global_variables(self) -> Dict[str, object]:
        """
        The current globals dictionary
        """
        return _global_variables

    @property
    def input_nodes(self) -> Mapping[LineaID, object]:
        """
        Returns a mapping of input node IDs to their objects
        """
        return {
            id_: self.global_variables[name]
            for name, id_ in self._input_node_ids.items()
        }


def set_context(
    executor: Executor,
    variables: Optional[Dict[str, LineaID]],
    node: CallNode,
) -> None:
    """
    Sets the context of the executor to the given node.
    """
    global _current_context
    if _current_context:
        raise RuntimeError("Context already set")

    # Set up our global variables, by first clearing out the old, and then
    # by updating with our new inputs
    # Note: We need to save our inputs so that we can check what has changed
    # at the end
    assert not _global_variables
    # The first time this is run, variables is set, and we know
    # the scoping, so we set all of the variables we know.
    # The subsequent times, we only use those that were recorded
    input_node_ids = variables or node.global_reads
    input_globals = {
        k: executor._id_to_value[id_] for k, id_ in input_node_ids.items()
    }

    _global_variables.setup_globals(input_globals)

    _current_context = ExecutionContext(
        node=node,
        executor=executor,
        _input_node_ids=input_node_ids,
        _input_globals_mutable={
            k: is_mutable(v) for k, v in input_globals.items()
        },
    )


def get_context() -> ExecutionContext:
    if not _current_context:
        raise RuntimeError("No context set")

    return _current_context


def teardown_context() -> ContextResult:
    """
    Tearsdown the context, returning the nodes that were accessed
    and a mapping variables to new values that were added or crated
    """
    global _current_context
    if not _current_context:
        raise RuntimeError("No context set")
    res = _global_variables.teardown_globals()
    prev_context = _current_context
    _current_context = None
    side_effects = prev_context.side_effects
    side_effects.extend(_compute_side_effects(prev_context, res))
    return ContextResult(res.added_or_modified, side_effects)


def _compute_side_effects(
    context: ExecutionContext, globals_result: GlobalsDictResult
) -> Iterable[SideEffect]:
    # Any nodes that we retrieved that were mutable, assume were mutated
    # Filter the vars by if the value is mutable
    mutable_input_vars: List[ExecutorPointer] = [
        ID(context._input_node_ids[name])
        for name in globals_result.accessed_inputs
        if context._input_globals_mutable[name]
    ]
    accessed_globals = AccessedGlobals(
        globals_result.accessed_inputs,
        list(globals_result.added_or_modified.keys()),
    )
    if accessed_globals.added_or_updated or accessed_globals.retrieved:
        yield accessed_globals

    yield from map(MutatedNode, mutable_input_vars)

    # Now we mark all the mutable input variables as well as mutable
    # output variables as all views of one another
    # Note that we retrieve the input IDs before executing,
    # and refer to the output IDs as variables after executing
    # This will mean any accessed mutable variables will resolve
    # to the node they pointed to before the function call
    # and mutated ones will refer to the new GlobalNodes that
    # were created when processing `AccessedGlobals`

    mutable_output_vars: List[ExecutorPointer] = [
        Variable(k)
        for k, v in globals_result.added_or_modified.items()
        if is_mutable(v)
    ]
    input_output_vars_view = ViewOfNodes(
        mutable_input_vars + mutable_output_vars
    )
    if len(input_output_vars_view.pointers) > 1:
        yield input_output_vars_view


@dataclass
class ContextResult:
    # Mapping of global name to value for every global which was added or updated
    added_or_modified: Dict[str, object]
    # List of side effects added during the execution.
    side_effects: SideEffects
