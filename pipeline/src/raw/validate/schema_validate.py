from pipeline.src.raw.validate.schema_version import EventoSchema_V1, ProductSchema_V1, StoreSchema_V1

from pydantic import ValidationError

# Valida cada linha

def schema_event_validation(linha):

    try:

        EventoSchema_V1(**linha)

        return "EventoSchema_V1", "VALIDO", None


    except ValidationError as e:

        return "EventoSchema_V1", "INVALIDO", str(e)
    

def schema_product_validation(linha):

    try:

        ProductSchema_V1(**linha)

        return "ProductSchema_V1", "VALIDO", None


    except ValidationError as e:

        return "ProductSchema_V1", "INVALIDO", str(e)
    

def schema_store_validation(linha):

    try:

        StoreSchema_V1(**linha)

        return "StoreSchema_V1", "VALIDO", None


    except ValidationError as e:

        return "StoreSchema_V1", "INVALIDO", str(e)