from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EducationalObjective(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    KNOW_AND_UNDERSTAND: _ClassVar[EducationalObjective]
    APPLY: _ClassVar[EducationalObjective]
    ANALYZE: _ClassVar[EducationalObjective]
    SYNTHESIZE: _ClassVar[EducationalObjective]
    EVALUATE: _ClassVar[EducationalObjective]
    INNOVATE: _ClassVar[EducationalObjective]

class Relationship(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SIMILARITY: _ClassVar[Relationship]
    DIFFERENCES: _ClassVar[Relationship]
    ORDER: _ClassVar[Relationship]
    COMPLEX: _ClassVar[Relationship]

class QuestionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MULTIPLE_CHOICE: _ClassVar[QuestionType]
    MULTIPLE_RESPONSE: _ClassVar[QuestionType]

class ModuleStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    RUNNING: _ClassVar[ModuleStatus]
    FAILED: _ClassVar[ModuleStatus]
    SUCCESS: _ClassVar[ModuleStatus]

class PipelineModule(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CONFIG_DESERIALIZATION: _ClassVar[PipelineModule]
    MATERIAL_FILTER: _ClassVar[PipelineModule]
    QUESTION_GENERATION: _ClassVar[PipelineModule]
    QUESTION_SPECIFICATION_MERGE: _ClassVar[PipelineModule]
    QUESTION_EVALUATION: _ClassVar[PipelineModule]
    QUESTION_DROP: _ClassVar[PipelineModule]
    CONFIG_MERGE: _ClassVar[PipelineModule]
    CONFIG_SERIALIZATION: _ClassVar[PipelineModule]
KNOW_AND_UNDERSTAND: EducationalObjective
APPLY: EducationalObjective
ANALYZE: EducationalObjective
SYNTHESIZE: EducationalObjective
EVALUATE: EducationalObjective
INNOVATE: EducationalObjective
SIMILARITY: Relationship
DIFFERENCES: Relationship
ORDER: Relationship
COMPLEX: Relationship
MULTIPLE_CHOICE: QuestionType
MULTIPLE_RESPONSE: QuestionType
RUNNING: ModuleStatus
FAILED: ModuleStatus
SUCCESS: ModuleStatus
CONFIG_DESERIALIZATION: PipelineModule
MATERIAL_FILTER: PipelineModule
QUESTION_GENERATION: PipelineModule
QUESTION_SPECIFICATION_MERGE: PipelineModule
QUESTION_EVALUATION: PipelineModule
QUESTION_DROP: PipelineModule
CONFIG_MERGE: PipelineModule
CONFIG_SERIALIZATION: PipelineModule

class String(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, value: _Optional[_Iterable[str]] = ...) -> None: ...

class ListOfStrings(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class MaterialUploadData(_message.Message):
    __slots__ = ["lecture_material", "data"]
    LECTURE_MATERIAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    lecture_material: LectureMaterial
    data: bytes
    def __init__(self, lecture_material: _Optional[_Union[LectureMaterial, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class InternalConfig(_message.Message):
    __slots__ = ["material_server_urls", "batches", "course_settings", "generation_settings", "evaluation_settings"]
    MATERIAL_SERVER_URLS_FIELD_NUMBER: _ClassVar[int]
    BATCHES_FIELD_NUMBER: _ClassVar[int]
    COURSE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    GENERATION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    material_server_urls: _containers.RepeatedScalarFieldContainer[str]
    batches: _containers.RepeatedCompositeFieldContainer[Batch]
    course_settings: CourseSettings
    generation_settings: GenerationSettings
    evaluation_settings: EvaluationSettings
    def __init__(self, material_server_urls: _Optional[_Iterable[str]] = ..., batches: _Optional[_Iterable[_Union[Batch, _Mapping]]] = ..., course_settings: _Optional[_Union[CourseSettings, _Mapping]] = ..., generation_settings: _Optional[_Union[GenerationSettings, _Mapping]] = ..., evaluation_settings: _Optional[_Union[EvaluationSettings, _Mapping]] = ...) -> None: ...

class CourseSettings(_message.Message):
    __slots__ = ["course_goals", "required_capabilites", "advantageous_capabilities"]
    COURSE_GOALS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_CAPABILITES_FIELD_NUMBER: _ClassVar[int]
    ADVANTAGEOUS_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    course_goals: _containers.RepeatedCompositeFieldContainer[Capability]
    required_capabilites: _containers.RepeatedCompositeFieldContainer[Capability]
    advantageous_capabilities: _containers.RepeatedCompositeFieldContainer[Capability]
    def __init__(self, course_goals: _Optional[_Iterable[_Union[Capability, _Mapping]]] = ..., required_capabilites: _Optional[_Iterable[_Union[Capability, _Mapping]]] = ..., advantageous_capabilities: _Optional[_Iterable[_Union[Capability, _Mapping]]] = ...) -> None: ...

class Capability(_message.Message):
    __slots__ = ["keywords", "educational_objective", "relationship"]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    EDUCATIONAL_OBJECTIVE_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    keywords: _containers.RepeatedScalarFieldContainer[str]
    educational_objective: EducationalObjective
    relationship: Relationship
    def __init__(self, keywords: _Optional[_Iterable[str]] = ..., educational_objective: _Optional[_Union[EducationalObjective, str]] = ..., relationship: _Optional[_Union[Relationship, str]] = ...) -> None: ...

class GenerationSettings(_message.Message):
    __slots__ = ["mode"]
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: Mode
    def __init__(self, mode: _Optional[_Union[Mode, _Mapping]] = ...) -> None: ...

class Mode(_message.Message):
    __slots__ = ["complete", "overwrite", "by_metrics"]
    COMPLETE_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    BY_METRICS_FIELD_NUMBER: _ClassVar[int]
    complete: Complete
    overwrite: Overwrite
    by_metrics: ByMetrics
    def __init__(self, complete: _Optional[_Union[Complete, _Mapping]] = ..., overwrite: _Optional[_Union[Overwrite, _Mapping]] = ..., by_metrics: _Optional[_Union[ByMetrics, _Mapping]] = ...) -> None: ...

class Complete(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Overwrite(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ByMetrics(_message.Message):
    __slots__ = ["arithmeticExpression"]
    ARITHMETICEXPRESSION_FIELD_NUMBER: _ClassVar[int]
    arithmeticExpression: str
    def __init__(self, arithmeticExpression: _Optional[str] = ...) -> None: ...

class EvaluationSettings(_message.Message):
    __slots__ = ["metrics"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[Metric]
    def __init__(self, metrics: _Optional[_Iterable[_Union[Metric, _Mapping]]] = ...) -> None: ...

class Question(_message.Message):
    __slots__ = ["question_type", "result", "evaluation"]
    QUESTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    question_type: QuestionType
    result: Result
    evaluation: Evaluation
    def __init__(self, question_type: _Optional[_Union[QuestionType, str]] = ..., result: _Optional[_Union[Result, _Mapping]] = ..., evaluation: _Optional[_Union[Evaluation, _Mapping]] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["multiple_choice", "multiple_response"]
    MULTIPLE_CHOICE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    multiple_choice: MultipleChoice
    multiple_response: MultipleResponse
    def __init__(self, multiple_choice: _Optional[_Union[MultipleChoice, _Mapping]] = ..., multiple_response: _Optional[_Union[MultipleResponse, _Mapping]] = ...) -> None: ...

class MultipleChoice(_message.Message):
    __slots__ = ["question_text", "answer_text", "distractor_text"]
    QUESTION_TEXT_FIELD_NUMBER: _ClassVar[int]
    ANSWER_TEXT_FIELD_NUMBER: _ClassVar[int]
    DISTRACTOR_TEXT_FIELD_NUMBER: _ClassVar[int]
    question_text: str
    answer_text: str
    distractor_text: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, question_text: _Optional[str] = ..., answer_text: _Optional[str] = ..., distractor_text: _Optional[_Iterable[str]] = ...) -> None: ...

class MultipleResponse(_message.Message):
    __slots__ = ["question_text", "answer_texts", "distractor_texts"]
    QUESTION_TEXT_FIELD_NUMBER: _ClassVar[int]
    ANSWER_TEXTS_FIELD_NUMBER: _ClassVar[int]
    DISTRACTOR_TEXTS_FIELD_NUMBER: _ClassVar[int]
    question_text: str
    answer_texts: _containers.RepeatedScalarFieldContainer[str]
    distractor_texts: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, question_text: _Optional[str] = ..., answer_texts: _Optional[_Iterable[str]] = ..., distractor_texts: _Optional[_Iterable[str]] = ...) -> None: ...

class Evaluation(_message.Message):
    __slots__ = ["reference", "result"]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    reference: str
    result: _any_pb2.Any
    def __init__(self, reference: _Optional[str] = ..., result: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class Metric(_message.Message):
    __slots__ = ["reference", "mode", "evaluation_type"]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    reference: str
    mode: Mode
    evaluation_type: EvaluationType
    def __init__(self, reference: _Optional[str] = ..., mode: _Optional[_Union[Mode, _Mapping]] = ..., evaluation_type: _Optional[_Union[EvaluationType, _Mapping]] = ...) -> None: ...

class EvaluationType(_message.Message):
    __slots__ = ["language_model_evaluation"]
    LANGUAGE_MODEL_EVALUATION_FIELD_NUMBER: _ClassVar[int]
    language_model_evaluation: LanguageModelEvaluation
    def __init__(self, language_model_evaluation: _Optional[_Union[LanguageModelEvaluation, _Mapping]] = ...) -> None: ...

class LanguageModelEvaluation(_message.Message):
    __slots__ = ["evaluationQuestion", "examples", "result_type"]
    EVALUATIONQUESTION_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    evaluationQuestion: str
    examples: _containers.RepeatedCompositeFieldContainer[Question]
    result_type: ResultType
    def __init__(self, evaluationQuestion: _Optional[str] = ..., examples: _Optional[_Iterable[_Union[Question, _Mapping]]] = ..., result_type: _Optional[_Union[ResultType, _Mapping]] = ...) -> None: ...

class ResultType(_message.Message):
    __slots__ = ["value_range", "categorical"]
    VALUE_RANGE_FIELD_NUMBER: _ClassVar[int]
    CATEGORICAL_FIELD_NUMBER: _ClassVar[int]
    value_range: ValueRange
    categorical: Categorical
    def __init__(self, value_range: _Optional[_Union[ValueRange, _Mapping]] = ..., categorical: _Optional[_Union[Categorical, _Mapping]] = ...) -> None: ...

class ValueRange(_message.Message):
    __slots__ = ["lowerBound", "upperBound"]
    LOWERBOUND_FIELD_NUMBER: _ClassVar[int]
    UPPERBOUND_FIELD_NUMBER: _ClassVar[int]
    lowerBound: float
    upperBound: float
    def __init__(self, lowerBound: _Optional[float] = ..., upperBound: _Optional[float] = ...) -> None: ...

class Categorical(_message.Message):
    __slots__ = ["categories"]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    categories: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, categories: _Optional[_Iterable[str]] = ...) -> None: ...

class Batch(_message.Message):
    __slots__ = ["lecture_materials", "question_to_generate", "capabilites"]
    LECTURE_MATERIALS_FIELD_NUMBER: _ClassVar[int]
    QUESTION_TO_GENERATE_FIELD_NUMBER: _ClassVar[int]
    CAPABILITES_FIELD_NUMBER: _ClassVar[int]
    lecture_materials: _containers.RepeatedCompositeFieldContainer[LectureMaterial]
    question_to_generate: _containers.RepeatedCompositeFieldContainer[Question]
    capabilites: _containers.RepeatedCompositeFieldContainer[Capability]
    def __init__(self, lecture_materials: _Optional[_Iterable[_Union[LectureMaterial, _Mapping]]] = ..., question_to_generate: _Optional[_Iterable[_Union[Question, _Mapping]]] = ..., capabilites: _Optional[_Iterable[_Union[Capability, _Mapping]]] = ...) -> None: ...

class LectureMaterial(_message.Message):
    __slots__ = ["reference", "url", "hash", "file_type", "page_filter"]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FILTER_FIELD_NUMBER: _ClassVar[int]
    reference: str
    url: str
    hash: str
    file_type: str
    page_filter: PageFilter
    def __init__(self, reference: _Optional[str] = ..., url: _Optional[str] = ..., hash: _Optional[str] = ..., file_type: _Optional[str] = ..., page_filter: _Optional[_Union[PageFilter, _Mapping]] = ...) -> None: ...

class PageFilter(_message.Message):
    __slots__ = ["lowerBound", "upperBound"]
    LOWERBOUND_FIELD_NUMBER: _ClassVar[int]
    UPPERBOUND_FIELD_NUMBER: _ClassVar[int]
    lowerBound: int
    upperBound: int
    def __init__(self, lowerBound: _Optional[int] = ..., upperBound: _Optional[int] = ...) -> None: ...

class PipelineStatus(_message.Message):
    __slots__ = ["result", "batch_status"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BATCH_STATUS_FIELD_NUMBER: _ClassVar[int]
    result: _any_pb2.Any
    batch_status: _containers.RepeatedCompositeFieldContainer[BatchStatus]
    def __init__(self, result: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., batch_status: _Optional[_Iterable[_Union[BatchStatus, _Mapping]]] = ...) -> None: ...

class BatchStatus(_message.Message):
    __slots__ = ["error_message", "pipeline_module"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_MODULE_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    pipeline_module: PipelineModule
    def __init__(self, error_message: _Optional[str] = ..., pipeline_module: _Optional[_Union[PipelineModule, str]] = ...) -> None: ...
