from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse
from src.application.use_cases.analyse_text_use_case import AnalyzeTextUseCase
from src.domain.services.text_analysis_service import TextAnalysisService
from src.insfrastructure.agents.contradiction_detector_agent import ContradictionDetector
from src.insfrastructure.agents.sentence_classifier_agent import SentenceClassifier
from src.insfrastructure.config.settings import AzureOpenAISettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


def main():
    request = AnalysisRequest(sentences=[
        "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري، حيث أن المشروع جاهز من الناحية الفنية، وتأخير القرار قد يؤدي إلى خسارة فرص استراتيجية مهمة.",
        "أرى رفض المقترح في الوقت الحالي بسبب عدم وضوح التكلفة الإجمالية والمخاطر التشغيلية، وأقترح إعادة الدراسة قبل اتخاذ أي قرار.",
        "أوصي باعتماد المقترح مع البدء بتطبيقه على نطاق محدود لمدة 3 أشهر لقياس الأثر قبل التوسع الكامل.",
        "أؤيد الموافقة على المقترح ولكن أرى أن تكون مدة التجربة سنة كاملة لضمان الحصول على نتائج دقيقة وشاملة.",
        "أرى أن المقترح مناسب من حيث المبدأ، ولكن يحتاج إلى تعديل في نطاق التنفيذ ليشمل عددًا أقل من الجهات في المرحلة الأولى.",
        "المقترح جيد، وأوصي بالمضي قدمًا مع تعديل بعض التفاصيل التشغيلية دون تغيير الهدف الرئيسي.",
        "أوصي بالموافقة على المقترح وتنفيذه تدريجيًا مع متابعة مؤشرات الأداء لضمان تحقيق الأهداف.",
        "أؤيد اعتماد المقترح مع تنفيذ مرحلي ومراقبة الأداء لضمان جودة النتائج."
    ])
    azure_settings = AzureOpenAISettings()
    prompt_provider = PromptyLoader()
    classifier_agent = SentenceClassifier(azure_settings, prompt_provider)
    detector_agent = ContradictionDetector(azure_settings, prompt_provider)
    text_analysis_service = TextAnalysisService(classifier_agent, detector_agent)
    analyze_text_use_case = AnalyzeTextUseCase(text_analysis_service)

    response: AnalysisResponse = analyze_text_use_case.execute(request)
    print(response)

if __name__ == "__main__":
    main()