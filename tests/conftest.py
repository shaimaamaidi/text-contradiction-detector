"""
Module: conftest
Description:
    Pytest configuration and shared fixtures for all test files.
    Provides test data fixtures with Arabic sentences for recommendation analysis and contradiction detection.
"""

import pytest


@pytest.fixture
def sample_sentences():
    """
    Fixture containing Arabic test sentences with recommendations and opinions.
    """
    return [
        "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري، حيث أن المشروع جاهز من الناحية الفنية، وتأخير القرار قد يؤدي إلى خسارة فرص استراتيجية مهمة.",
        "أرى رفض المقترح في الوقت الحالي بسبب عدم وضوح التكلفة الإجمالية والمخاطر التشغيلية، وأقترح إعادة الدراسة قبل اتخاذ أي قرار.",
        "أوصي باعتماد المقترح مع البدء بتطبيقه على نطاق محدود لمدة 3 أشهر لقياس الأثر قبل التوسع الكامل.",
        "أؤيد الموافقة على المقترح ولكن أرى أن تكون مدة التجربة سنة كاملة لضمان الحصول على نتائج دقيقة وشاملة.",
        "أرى أن المقترح مناسب من حيث المبدأ، ولكن يحتاج إلى تعديل في نطاق التنفيذ ليشمل عددًا أقل من الجهات في المرحلة الأولى.",
        "المقترح جيد، وأوصي بالمضي قدمًا مع تعديل بعض التفاصيل التشغيلية دون تغيير الهدف الرئيسي.",
        "أوصي بالموافقة على المقترح وتنفيذه تدريجيًا مع متابعة مؤشرات الأداء لضمان تحقيق الأهداف.",
        "أؤيد اعتماد المقترح مع تنفيذ مرحلي ومراقبة الأداء لضمان جودة النتائج.",
        "أوصي بالاستثمار في الطاقة الشمسية لتقليل التكاليف وزيادة الاستدامة.",
        "أرى أن التركيز على الوقود الأحفوري أكثر أمانًا وموثوقية لتلبية احتياجات الطاقة الحالية.",
    ]


@pytest.fixture
def analysis_request_data(sample_sentences):
    """
    Fixture for an analysis request with test sentences.
    """
    return {
        "sentences": sample_sentences
    }


@pytest.fixture
def sample_single_sentence():
    """
    Fixture for a single test sentence.
    """
    return "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري."


@pytest.fixture
def contradictory_sentences():
    """
    Fixture containing pairs of contradictory sentences.
    """
    return [
        "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري.",
        "أرى رفض المقترح في الوقت الحالي بسبب عدم وضوح التكلفة الإجمالية."
    ]


@pytest.fixture
def non_contradictory_sentences():
    """
    Fixture containing non-contradictory sentences.
    """
    return [
        "أوصي باعتماد المقترح مع البدء بتطبيقه على نطاق محدود.",
        "المقترح جيد، وأوصي بالمضي قدمًا مع تعديل بعض التفاصيل."
    ]


@pytest.fixture
def empty_sentences():
    """
    Fixture for an empty case.
    """
    return []
