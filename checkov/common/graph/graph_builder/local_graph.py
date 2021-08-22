from abc import abstractmethod
from collections import defaultdict
from typing import List, Dict, Callable, Union, Any, Optional

from checkov.common.graph.graph_builder import Edge
from checkov.common.graph.graph_builder.graph_components.blocks import Block


class LocalGraph:
    def __init__(self) -> None:
        self.vertices: List[Block] = []
        self.edges: List[Edge] = []
        self.in_edges: Dict[int, List[Edge]] = defaultdict(list)  # map between vertex index and the edges entering it
        self.out_edges: Dict[int, List[Edge]] = defaultdict(list)  # map between vertex index and the edges exiting it
        self.vertices_by_block_type: Dict[str, List[int]] = defaultdict(list)
        self.vertex_hash_cache: Dict[int, str] = defaultdict(str)
        self.vertices_block_name_map: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: defaultdict(list))

    @abstractmethod
    def build_graph(self, render_variables: bool) -> None:
        pass

    def get_vertices_with_degrees_conditions(
        self, out_degree_cond: Callable[[int], bool], in_degree_cond: Callable[[int], bool]
    ) -> List[int]:
        vertices_with_out_degree = {
            vertex_index for vertex_index in self.out_edges.keys() if out_degree_cond(len(self.out_edges[vertex_index]))
        }
        vertices_with_in_degree = {
            vertex_index for vertex_index in self.in_edges.keys() if in_degree_cond(len(self.in_edges[vertex_index]))
        }

        return list(vertices_with_in_degree.intersection(vertices_with_out_degree))

    def get_in_edges(self, end_vertices: List[int]) -> List[Edge]:
        res = []
        for vertex in end_vertices:
            res.extend(self.in_edges.get(vertex, []))
        return self.sort_edged_by_dest_out_degree(res)

    def sort_edged_by_dest_out_degree(self, edges: List[Edge]) -> List[Edge]:
        edged_by_out_degree: Dict[int, List[Edge]] = {}
        for edge in edges:
            dest_out_degree = len(self.out_edges[edge.dest])
            edged_by_out_degree.setdefault(dest_out_degree, []).append(edge)
        sorted_edges = []
        for degree in sorted(edged_by_out_degree.keys()):
            sorted_edges.extend(edged_by_out_degree[degree])
        return sorted_edges

    @abstractmethod
    def update_vertices_configs(self) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def update_vertex_config(vertex: Block, changed_attributes: Union[List[str], Dict[str, Any]]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_resources_types_in_graph(self) -> List[str]:
        raise NotImplementedError()

    def get_vertex_attributes_by_index(self, index: int) -> Dict[str, Any]:
        return self.vertices[index].get_attribute_dict()

    @abstractmethod
    def update_vertex_attribute(
        self,
        vertex_index: int,
        attribute_key: str,
        attribute_value: Any,
        change_origin_id: int,
        attribute_at_dest: Optional[Union[str, List[str]]],
    ) -> None:
        raise NotImplementedError()
