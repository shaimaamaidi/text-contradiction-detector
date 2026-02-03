"""
Module: test_contradiction_llm_response
Description:
    Unit tests for ContradictionLLM and ContradictionLLMResponse models.
    Tests serialization, deserialization, and field aliases in Arabic.
"""

import pytest
from src.domain.models.contradiction_llm_response import ContradictionLLM, ContradictionLLMResponse


class TestContradictionLLM:
    """
    Unit tests for the ContradictionLLM model.
    """

    def test_contradiction_llm_creation_with_english_fields(self):
        """
        Test creation of ContradictionLLM using English field names.
        """
        # Arrange
        statements = [1, 2]
        severity_level = "حاد"
        comment = "Test contradiction"

        # Act
        contradiction = ContradictionLLM(
            statements=statements,
            severity_level=severity_level,
            comment=comment
        )

        # Assert
        assert contradiction.statements == statements
        assert contradiction.severity_level == severity_level
        assert contradiction.comment == comment

    def test_contradiction_llm_creation_with_arabic_aliases(self):
        """
        Test creation of ContradictionLLM using Arabic field aliases.
        """
        # Arrange
        data = {
            "إفادات": [1, 2],
            "مستوى_التعارض": "متوسط",
            "تعليق": "اختبار التناقض"
        }

        # Act
        contradiction = ContradictionLLM(**data)

        # Assert
        assert contradiction.statements == [1, 2]
        assert contradiction.severity_level == "متوسط"
        assert contradiction.comment == "اختبار التناقض"

    def test_contradiction_llm_serialization_to_dict(self):
        """
        Test serialization of ContradictionLLM to dictionary.
        """
        # Arrange
        contradiction = ContradictionLLM(
            statements=[1, 2],
            severity_level="حاد",
            comment="Test"
        )

        # Act
        data = contradiction.model_dump()

        # Assert
        assert "statements" in data
        assert data["statements"] == [1, 2]

    def test_contradiction_llm_serialization_with_alias(self):
        """
        Test serialization of ContradictionLLM with Arabic aliases.
        """
        # Arrange
        contradiction = ContradictionLLM(
            statements=[1, 3],
            severity_level="متوسط",
            comment="اختبار"
        )

        # Act
        data = contradiction.model_dump(by_alias=True)

        # Assert
        assert "إفادات" in data
        assert data["إفادات"] == [1, 3]
        assert "مستوى_التعارض" in data
        assert data["مستوى_التعارض"] == "متوسط"
        assert "تعليق" in data
        assert data["تعليق"] == "اختبار"

    def test_contradiction_llm_severity_levels(self):
        """
        Test ContradictionLLM with different severity levels.
        """
        # Arrange & Act
        contradiction_severe = ContradictionLLM(
            statements=[1, 2],
            severity_level="حاد",
            comment="Severe"
        )
        contradiction_moderate = ContradictionLLM(
            statements=[2, 3],
            severity_level="متوسط",
            comment="Moderate"
        )

        # Assert
        assert contradiction_severe.severity_level == "حاد"
        assert contradiction_moderate.severity_level == "متوسط"

    def test_contradiction_llm_multiple_statements(self):
        """
        Test ContradictionLLM with multiple statement indices.
        """
        # Arrange
        statements = [1, 2, 3, 4]

        # Act
        contradiction = ContradictionLLM(
            statements=statements,
            severity_level="حاد",
            comment="Multiple statements"
        )

        # Assert
        assert len(contradiction.statements) == 4
        assert contradiction.statements == statements


class TestContradictionLLMResponse:
    """
    Unit tests for the ContradictionLLMResponse model.
    """

    def test_contradiction_llm_response_creation_with_english_fields(self):
        """
        Test creation of ContradictionLLMResponse using English field names.
        """
        # Arrange
        contradictions = [
            ContradictionLLM(statements=[1, 2], severity_level="حاد", comment="Test 1"),
            ContradictionLLM(statements=[2, 3], severity_level="متوسط", comment="Test 2")
        ]

        # Act
        response = ContradictionLLMResponse(contradictions=contradictions)

        # Assert
        assert len(response.contradictions) == 2
        assert response.contradictions[0].statements == [1, 2]
        assert response.contradictions[1].statements == [2, 3]

    def test_contradiction_llm_response_creation_with_arabic_alias(self):
        """
        Test creation of ContradictionLLMResponse using Arabic alias.
        """
        # Arrange
        data = {
            "التناقضات": [
                {
                    "إفادات": [1, 2],
                    "مستوى_التعارض": "حاد",
                    "تعليق": "التناقض الأول"
                },
                {
                    "إفادات": [3, 4],
                    "مستوى_التعارض": "متوسط",
                    "تعليق": "التناقض الثاني"
                }
            ]
        }

        # Act
        response = ContradictionLLMResponse(**data)

        # Assert
        assert len(response.contradictions) == 2
        assert response.contradictions[0].statements == [1, 2]
        assert response.contradictions[0].severity_level == "حاد"
        assert response.contradictions[0].comment == "التناقض الأول"
        assert response.contradictions[1].statements == [3, 4]

    def test_contradiction_llm_response_empty_contradictions(self):
        """
        Test creation of ContradictionLLMResponse with empty contradictions list.
        """
        # Arrange
        response = ContradictionLLMResponse(contradictions=[])

        # Assert
        assert len(response.contradictions) == 0

    def test_contradiction_llm_response_serialization(self):
        """
        Test serialization of ContradictionLLMResponse to dictionary.
        """
        # Arrange
        contradictions = [
            ContradictionLLM(statements=[1, 2], severity_level="حاد", comment="Test")
        ]
        response = ContradictionLLMResponse(contradictions=contradictions)

        # Act
        data = response.model_dump()

        # Assert
        assert "contradictions" in data
        assert len(data["contradictions"]) == 1

    def test_contradiction_llm_response_serialization_with_alias(self):
        """
        Test serialization of ContradictionLLMResponse with Arabic aliases.
        """
        # Arrange
        contradictions = [
            ContradictionLLM(statements=[1, 2], severity_level="حاد", comment="Test 1"),
            ContradictionLLM(statements=[3, 4], severity_level="متوسط", comment="Test 2")
        ]
        response = ContradictionLLMResponse(contradictions=contradictions)

        # Act
        data = response.model_dump(by_alias=True)

        # Assert
        assert "التناقضات" in data
        assert len(data["التناقضات"]) == 2
        assert data["التناقضات"][0]["إفادات"] == [1, 2]
        assert data["التناقضات"][0]["مستوى_التعارض"] == "حاد"
        assert data["التناقضات"][1]["إفادات"] == [3, 4]

    def test_contradiction_llm_response_json_schema(self):
        """
        Test that ContradictionLLMResponse generates correct JSON schema.
        """
        # Act
        schema = ContradictionLLMResponse.model_json_schema()

        # Assert
        assert "properties" in schema
        # The alias in Arabic is used in the schema
        assert "التناقضات" in schema["properties"]

    def test_contradiction_llm_response_populate_by_name(self):
        """
        Test that populate_by_name allows both field names and aliases.
        """
        # Arrange - Data with English field names
        data_english = {
            "contradictions": [
                {
                    "statements": [1, 2],
                    "severity_level": "حاد",
                    "comment": "Test"
                }
            ]
        }

        # Act
        response = ContradictionLLMResponse(**data_english)

        # Assert
        assert len(response.contradictions) == 1
        assert response.contradictions[0].statements == [1, 2]

    def test_contradiction_llm_response_multiple_contradictions(self):
        """
        Test ContradictionLLMResponse with multiple contradictions.
        """
        # Arrange
        contradictions_data = [
            {"statements": [1, 2], "severity_level": "حاد", "comment": "High severity"},
            {"statements": [2, 3], "severity_level": "متوسط", "comment": "Medium severity"},
            {"statements": [4, 5], "severity_level": "حاد", "comment": "High severity again"}
        ]
        contradictions = [ContradictionLLM(**data) for data in contradictions_data]

        # Act
        response = ContradictionLLMResponse(contradictions=contradictions)

        # Assert
        assert len(response.contradictions) == 3
        assert all(c.severity_level in ["حاد", "متوسط"] for c in response.contradictions)
