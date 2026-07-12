# Base das exceptions

class PipelineBusinessException(Exception):
    def __init__(self, arquivo, entidade, inicio, status, motivo, mensagem):
        self.arquivo = arquivo
        self.entidade = entidade
        self.inicio = inicio
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