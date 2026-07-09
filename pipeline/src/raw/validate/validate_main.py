from pipeline.src.raw.validate.schema_validate import schema_event_validation, schema_product_validation, schema_store_validation

# Valida schema de um registro

def validate_schema(registro, entidade):

    try:

        if entidade == "eventos":
            versao_schema, status, validation_error = schema_event_validation(registro)
            return versao_schema, status, validation_error
        
        elif entidade == "produtos":
            versao_schema, status, validation_error = schema_product_validation(registro)
            return versao_schema, status, validation_error

        elif entidade == "lojas":
            versao_schema, status, validation_error = schema_store_validation(registro)
            return versao_schema, status, validation_error
    
    except Exception as e:
        print(f"erro na validade_schema: {e}")
        raise