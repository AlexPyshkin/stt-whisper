from schemas import GateWayDTO
from typing import Optional, Dict, Any


def wrap_response(
    text: str,
    service_name: str = "sst-whisper",
    job_name: str = "",
    status_code: int = 200,
    success: bool = True,
    error_message: Optional[str] = None,
    job: Optional[Dict[str, Any]] = None
) -> GateWayDTO:
    """
    Оборачивает строку text в GateWayDTO, помещая её в jobTitle JobDTO.

    :param text: распознанный текст
    :param service_name: название сервиса
    :param job_name: название задачи
    :param status_code: HTTP статус код
    :param success: успех операции
    :param error_message: сообщение об ошибке
    :param job: доп. инфа по задаче
    :return: GateWayDTO
    """
    return GateWayDTO(
        serviceName=service_name,
        jobName=job_name,
        statusCode=status_code,
        success=success,
        errorMessage=error_message,
        responseBodyBatch=[
            text
        ],
        job=job
    )
