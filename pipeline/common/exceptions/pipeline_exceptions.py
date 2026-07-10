# Base das exceptions

class PipelineBusinessException(Exception):
    def __init__(self, arquivo, status, motivo, mensagem):
        self.arquivo = arquivo
        self.status = status
        self.motivo = motivo
        self.mensagem = mensagem

        super().__init__(mensagem)

# Raw exceptions

class UnknownEntityException(PipelineBusinessException):
    pass

class InvalidFileTypeException(PipelineBusinessException):
    pass

class DuplicateFileException(PipelineBusinessException):
    pass

class EmptyfileExcept(PipelineBusinessException):
    pass

class AllRecordsQuarantinedException(PipelineBusinessException):
    pass

class InsertRecordsFail(PipelineBusinessException):
    pass