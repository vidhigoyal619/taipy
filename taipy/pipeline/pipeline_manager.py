"""
Pipeline Manager is responsible for managing the pipelines.
This is the entry point for operations (such as creating, reading, updating, deleting, duplicating, executing) related
 to pipelines.
"""
from taipy.pipeline.types import PipelineId, Dag
from taipy.pipeline.pipeline import Pipeline
from taipy.pipeline.pipeline_model import PipelineModel
from taipy.pipeline.pipeline_schema import PipelineSchema
from taipy.task.task_manager import TaskManager


class PipelineManager:
    task_manager = TaskManager()

    def __init__(self):
        # This represents the pipeline database table.
        self.__PIPELINE_DB: dict[PipelineId, PipelineModel] = {}

    def save_pipeline(self, pipeline: Pipeline):
        self.__PIPELINE_DB[pipeline.id] = pipeline.to_model()

    def get_pipeline_schema(self, pipeline_id: PipelineId) -> PipelineSchema:
        model = self.__PIPELINE_DB[pipeline_id]
        return PipelineSchema(model.id, model.name, model.properties, Dag({**model.source_task_edges, **model.task_source_edges}))

    def get_pipeline(self, pipeline_id: PipelineId) -> Pipeline:
        model = self.__PIPELINE_DB[pipeline_id]
        tasks = list(map(self.task_manager.get_task, model.task_source_edges.keys()))
        return Pipeline(model.id, model.name, model.properties, tasks)

    def get_pipelines(self) -> list[Pipeline]:
        return [self.get_pipeline(model.id) for model in list(self.__PIPELINE_DB.values())]
