"""
Module: ai_question_generator/knowledge.py

Maps domain-specific tags (e.g., "git", "python") to their corresponding
knowledge base IDs in OpenWebUI or other vector stores.

Usage:
    knowledge_id = KNOWLEDGE_ID_MAP.get("python")
"""

KNOWLEDGE_ID_MAP = {
    "git": "8a810abf-8284-4839-bf56-5dbcf957c54e",
    "docker": "c5684210-5838-4188-b644-2356e7f732c6",
    "java": "a105cc3d-958e-4e2e-adfb-297d0b3cca9c",
    "mysql": "6da0f295-f0c0-488f-937e-d7fe66debe6c",
    "python": "88688bf7-5f65-4bf4-9af8-b389ba327e23",
    "javascript": "2e7034ef-c9ff-4166-9055-bedb86201817",
    "nodejs": "7033f227-f722-4124-9bab-d5bbe1daee4f",
    "c": "4bc68cc4-baf1-4316-bb9f-f4f3a7901ad6",
    "c++": "25431ed7-63f0-4397-b062-d31a235519be",
    "c#": "4b3f2942-3b07-4edf-abfc-59805a31799d",
    "php": "421c9fb7-aaf7-4571-bda4-5613f155362b",
    "hibernate": "1da5116a-b9ac-4381-828d-6517ec8c2d95",
    "spring": "3cd8876b-07d8-4d1b-9180-75ec310772a6",
    "angular": "ad269181-dfe0-4b3e-b1ca-2167517eb20e",
    "redis": "8e274f7d-069f-4255-9dbf-a59dd6c1858b",
    "go": "6da11c24-9679-4b97-9064-68b5184cff35",
    "reactjs": "24979538-87dd-45d4-8a81-1d434a6b2686",
    "typescript": "ffe513c1-8702-4b35-8ae9-df6c6b1fe079",
    "sql": "5ab39ed6-39cc-4260-82fb-2e3239d90be2",
    "ruby": "c0c6ade1-2e5d-48d0-8246-2464bfb92a2e",
    "rust": "76853723-7d0f-4884-bfd2-a50eb60f578e",
    "nginx": "b5194dc0-8a64-4675-958b-5d1e84f61912",
}
