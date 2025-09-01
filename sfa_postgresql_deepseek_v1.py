#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "openai>=1.63.0",
#   "psycopg2-binary>=2.9.0",
#   "rich>=13.7.0",
#   "pydantic>=2.0.0",
#   "python-dotenv>=1.0.0",
# ]
# ///

"""
================================================================================
                    SFA PostgreSQL Explorer con DeepSeek
================================================================================

Single File Agent para explorar y consultar bases de datos PostgreSQL usando
la API de DeepSeek. Basado en el patrón de sfa_duckdb_openai_v2.py

CARACTERÍSTICAS:
- Conexión directa a PostgreSQL
- Exploración de tablas y relaciones
- Pre-verificación de queries
- Prompts en español
- Usa DeepSeek API

USO:
    uv run sfa_postgresql_deepseek_v1.py -p "Lista todas las tablas" -c 10
    uv run sfa_postgresql_deepseek_v1.py -p "Muestra usuarios activos" -c 15

================================================================================
"""

import os
import sys
import json
import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import openai
from pydantic import BaseModel, Field, ValidationError

# Cargar variables de entorno
load_dotenv()

# Inicializar consola Rich
console = Console()

# ================================================================================
#                          CONFIGURACIÓN
# ================================================================================

# DeepSeek API Configuration
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# PostgreSQL Configuration - ACTUALIZA CON TUS CREDENCIALES
PG_CONFIG = {
    "host": "localhost",  # Cambiar por tu host
    "database": "red_mentores2",  # Cambiar por tu database
    "user": "pablozunigavalenzuela",  # Cambiar por tu usuario
    "password": "",  # Cambiar por tu password
    "port": 5432
}

# ================================================================================
#                      MODELOS PYDANTIC PARA HERRAMIENTAS
# ================================================================================

class ListarTablasArgs(BaseModel):
    razonamiento: str = Field(
        ..., description="Explicación de por qué necesitas listar las tablas"
    )


class DescribirTablaArgs(BaseModel):
    razonamiento: str = Field(
        ..., description="Razón por la cual necesitas el esquema de esta tabla"
    )
    nombre_tabla: str = Field(..., description="Nombre de la tabla a describir")


class MuestrearTablaArgs(BaseModel):
    razonamiento: str = Field(
        ..., description="Explicación de por qué necesitas muestrear esta tabla"
    )
    nombre_tabla: str = Field(..., description="Nombre de la tabla a muestrear")
    cantidad_filas: int = Field(
        default=5, description="Número de filas a muestrear (recomendado 3-5)"
    )


class ListarRelacionesArgs(BaseModel):
    razonamiento: str = Field(
        ..., description="Por qué necesitas conocer las relaciones"
    )
    nombre_tabla: str = Field(
        default=None, description="Tabla específica o None para todas"
    )


class EjecutarConsultaPruebaArgs(BaseModel):
    razonamiento: str = Field(
        ..., description="Razón para probar esta consulta"
    )
    consulta_sql: str = Field(..., description="La consulta SQL a probar")


class EjecutarConsultaFinalArgs(BaseModel):
    razonamiento: str = Field(
        ..., description="Explicación final de cómo esta consulta satisface el pedido"
    )
    consulta_sql: str = Field(..., description="La consulta SQL validada a ejecutar")


# ================================================================================
#                      FUNCIONES DE HERRAMIENTAS
# ================================================================================

def get_db_connection():
    """Crea una conexión a PostgreSQL con permisos de solo lectura."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        # Configurar la conexión como solo lectura
        with conn.cursor() as cur:
            cur.execute("SET default_transaction_read_only = ON;")
        conn.commit()
        return conn
    except Exception as e:
        console.print(f"[red]Error conectando a PostgreSQL: {str(e)}[/red]")
        raise


def listar_tablas(razonamiento: str) -> List[Dict[str, str]]:
    """Lista todas las tablas y vistas en la base de datos."""
    console.log(f"[blue]Listar Tablas[/blue] - Razonamiento: {razonamiento}")

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT
                        schemaname as esquema,
                        tablename as tabla,
                        'tabla' as tipo
                    FROM pg_tables
                    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                    UNION ALL
                    SELECT
                        schemaname as esquema,
                        viewname as tabla,
                        'vista' as tipo
                    FROM pg_views
                    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                    ORDER BY esquema, tabla;
                """)
                results = cur.fetchall()

                # Mostrar tabla bonita
                table = Table(title="Tablas y Vistas Disponibles")
                table.add_column("Esquema", style="cyan")
                table.add_column("Tabla/Vista", style="green")
                table.add_column("Tipo", style="yellow")

                for row in results:
                    table.add_row(row['esquema'], row['tabla'], row['tipo'])

                console.print(table)
                return results

    except Exception as e:
        console.print(f"[red]Error listando tablas: {str(e)}[/red]")
        return []


def describir_tabla(razonamiento: str, nombre_tabla: str) -> str:
    """Retorna información del esquema de la tabla especificada."""
    console.log(f"[blue]Describir Tabla[/blue] - Tabla: {nombre_tabla} - Razonamiento: {razonamiento}")

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Obtener columnas
                cur.execute("""
                    SELECT
                        column_name,
                        data_type,
                        character_maximum_length,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (nombre_tabla,))

                columns = cur.fetchall()

                if not columns:
                    return f"Tabla '{nombre_tabla}' no encontrada"

                # Obtener constraints
                cur.execute("""
                    SELECT
                        tc.constraint_name,
                        tc.constraint_type,
                        kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_name = %s;
                """, (nombre_tabla,))

                constraints = cur.fetchall()

                # Formatear resultado
                result = f"\n=== ESQUEMA DE TABLA: {nombre_tabla} ===\n\n"
                result += "COLUMNAS:\n"
                for col in columns:
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    length = f"({col['character_maximum_length']})" if col['character_maximum_length'] else ""
                    result += f"  - {col['column_name']}: {col['data_type']}{length} {nullable}\n"

                if constraints:
                    result += "\nCONSTRAINTS:\n"
                    for const in constraints:
                        result += f"  - {const['constraint_type']}: {const['column_name']} ({const['constraint_name']})\n"

                console.print(Panel(result, title=f"Esquema: {nombre_tabla}"))
                return result

    except Exception as e:
        error_msg = f"Error describiendo tabla: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        return error_msg


def muestrear_tabla(razonamiento: str, nombre_tabla: str, cantidad_filas: int = 5) -> str:
    """Retorna una muestra de filas de la tabla especificada."""
    console.log(f"[blue]Muestrear Tabla[/blue] - Tabla: {nombre_tabla} - Filas: {cantidad_filas} - Razonamiento: {razonamiento}")

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Usar comillas para manejar nombres de tabla con mayúsculas o caracteres especiales
                query = f'SELECT * FROM "{nombre_tabla}" LIMIT %s;'
                cur.execute(query, (cantidad_filas,))

                rows = cur.fetchall()

                if not rows:
                    return f"No se encontraron filas en la tabla '{nombre_tabla}'"

                # Formatear resultado como tabla
                result = f"\n=== MUESTRA DE TABLA: {nombre_tabla} ({len(rows)} filas) ===\n"
                result += json.dumps(rows, indent=2, default=str)

                console.print(Panel(result, title=f"Muestra: {nombre_tabla}"))
                return result

    except Exception as e:
        error_msg = f"Error muestreando tabla: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        return error_msg


def listar_relaciones(razonamiento: str, nombre_tabla: str = None) -> str:
    """Lista las relaciones (foreign keys) de la base de datos o de una tabla específica."""
    console.log(f"[blue]Listar Relaciones[/blue] - Tabla: {nombre_tabla or 'TODAS'} - Razonamiento: {razonamiento}")

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT
                        tc.table_name as tabla_origen,
                        kcu.column_name as columna_origen,
                        ccu.table_name as tabla_destino,
                        ccu.column_name as columna_destino,
                        tc.constraint_name as nombre_constraint
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                """

                if nombre_tabla:
                    query += " AND tc.table_name = %s"
                    cur.execute(query, (nombre_tabla,))
                else:
                    cur.execute(query)

                relations = cur.fetchall()

                if not relations:
                    return f"No se encontraron relaciones{' para ' + nombre_tabla if nombre_tabla else ''}"

                # Formatear resultado
                result = f"\n=== RELACIONES (FOREIGN KEYS) ===\n\n"
                for rel in relations:
                    result += f"{rel['tabla_origen']}.{rel['columna_origen']} -> {rel['tabla_destino']}.{rel['columna_destino']}\n"

                console.print(Panel(result, title="Relaciones"))
                return result

    except Exception as e:
        error_msg = f"Error listando relaciones: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        return error_msg


def ejecutar_consulta_prueba(razonamiento: str, consulta_sql: str) -> str:
    """Ejecuta una consulta SQL de prueba (solo visible para el agente)."""
    console.log(f"[blue]Consulta de Prueba[/blue] - Razonamiento: {razonamiento}")
    console.log(f"[dim]Query: {consulta_sql}[/dim]")

    # Verificar que sea una consulta SELECT (seguridad)
    if not consulta_sql.strip().upper().startswith('SELECT'):
        return "Error: Solo se permiten consultas SELECT"

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(consulta_sql)
                rows = cur.fetchall()

                result = f"Consulta ejecutada exitosamente. {len(rows)} filas retornadas.\n"
                if rows:
                    # Mostrar primeras 10 filas
                    result += json.dumps(rows[:10], indent=2, default=str)

                return result

    except Exception as e:
        error_msg = f"Error en consulta de prueba: {str(e)}"
        console.print(f"[yellow]{error_msg}[/yellow]")
        return error_msg


def ejecutar_consulta_final(razonamiento: str, consulta_sql: str) -> str:
    """Ejecuta la consulta SQL final y muestra los resultados al usuario."""
    console.log(
        Panel(
            f"[green]Consulta Final[/green]\nRazonamiento: {razonamiento}\nQuery: {consulta_sql}"
        )
    )

    # Verificar que sea una consulta SELECT (seguridad)
    if not consulta_sql.strip().upper().startswith('SELECT'):
        return "Error: Solo se permiten consultas SELECT"

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(consulta_sql)
                rows = cur.fetchall()

                if not rows:
                    return "La consulta no retornó resultados"

                # Crear tabla bonita para mostrar resultados
                if rows:
                    table = Table(title=f"Resultados ({len(rows)} filas)")

                    # Agregar columnas
                    for key in rows[0].keys():
                        table.add_column(key, style="cyan")

                    # Agregar filas (máximo 50 para no saturar)
                    for row in rows[:50]:
                        table.add_row(*[str(v) for v in row.values()])

                    console.print(table)

                    if len(rows) > 50:
                        console.print(f"[yellow]Mostrando solo las primeras 50 de {len(rows)} filas[/yellow]")

                # También retornar como JSON para el agente
                return json.dumps(rows, indent=2, default=str)

    except Exception as e:
        error_msg = f"Error en consulta final: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        return error_msg


# ================================================================================
#                      CONFIGURACIÓN DE HERRAMIENTAS
# ================================================================================

# Definir las herramientas para DeepSeek
tools = [
    {
        "type": "function",
        "function": {
            "name": "ListarTablasArgs",
            "description": "Lista todas las tablas y vistas disponibles en la base de datos",
            "parameters": ListarTablasArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "DescribirTablaArgs",
            "description": "Obtiene el esquema detallado de una tabla específica",
            "parameters": DescribirTablaArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "MuestrearTablaArgs",
            "description": "Obtiene una muestra de filas de una tabla",
            "parameters": MuestrearTablaArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ListarRelacionesArgs",
            "description": "Lista las relaciones (foreign keys) entre tablas",
            "parameters": ListarRelacionesArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "EjecutarConsultaPruebaArgs",
            "description": "Ejecuta una consulta SQL de prueba para validación",
            "parameters": EjecutarConsultaPruebaArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "EjecutarConsultaFinalArgs",
            "description": "Ejecuta la consulta SQL final validada",
            "parameters": EjecutarConsultaFinalArgs.model_json_schema()
        }
    }
]

# ================================================================================
#                      PROMPT DEL AGENTE
# ================================================================================

AGENT_PROMPT = """<propósito>
    Eres un experto en PostgreSQL especializado en explorar y consultar bases de datos.
    Tu objetivo es entender la estructura completa de la base de datos, sus relaciones,
    y generar consultas SQL precisas que satisfagan exactamente las necesidades del usuario.
</propósito>

<instrucciones>
    <instrucción>Usa las herramientas proporcionadas para explorar la base de datos y construir la consulta perfecta.</instrucción>
    <instrucción>Comienza listando las tablas para entender qué está disponible.</instrucción>
    <instrucción>Examina las relaciones entre tablas para entender cómo se conectan los datos.</instrucción>
    <instrucción>Describe las tablas relevantes para comprender su esquema y columnas.</instrucción>
    <instrucción>Muestrea las tablas para ver patrones de datos reales.</instrucción>
    <instrucción>SIEMPRE prueba las consultas antes de finalizarlas usando EjecutarConsultaPrueba.</instrucción>
    <instrucción>Solo llama a ejecutar_consulta_final cuando estés seguro de que la consulta es perfecta.</instrucción>
    <instrucción>Sé exhaustivo pero eficiente con el uso de herramientas.</instrucción>
    <instrucción>Si tu consulta de prueba retorna un error o no satisface el pedido, intenta corregirla.</instrucción>
    <instrucción>Piensa paso a paso sobre qué información necesitas.</instrucción>
    <instrucción>Asegúrate de especificar todos los parámetros en cada llamada de herramienta.</instrucción>
    <instrucción>Cada llamada de herramienta debe tener un parámetro 'razonamiento' donde expliques por qué la estás llamando.</instrucción>
</instrucciones>

<herramientas_disponibles>
    1. listar_tablas: Retorna lista de todas las tablas y vistas en la base de datos
    2. describir_tabla: Retorna información del esquema para una tabla específica
    3. muestrear_tabla: Retorna filas de ejemplo de una tabla específica
    4. listar_relaciones: Muestra las foreign keys y relaciones entre tablas
    5. ejecutar_consulta_prueba: Prueba una consulta SQL (solo visible para ti)
    6. ejecutar_consulta_final: Ejecuta la consulta SQL validada final
</herramientas_disponibles>

<pedido_usuario>
    {{pedido_usuario}}
</pedido_usuario>
"""

# ================================================================================
#                      FUNCIÓN PRINCIPAL
# ================================================================================

def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="Agente PostgreSQL con DeepSeek API")
    parser.add_argument(
        "-p", "--prompt", required=True, help="El pedido del usuario"
    )
    parser.add_argument(
        "-c",
        "--compute",
        type=int,
        default=10,
        help="Número máximo de iteraciones del agente (default: 10)",
    )
    args = parser.parse_args()

    # Obtener API key de DeepSeek
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    if not DEEPSEEK_API_KEY:
        console.print(
            "[red]Error: DEEPSEEK_API_KEY no está configurada en el entorno[/red]"
        )
        console.print(
            "Por favor configura tu API key: export DEEPSEEK_API_KEY='tu-api-key'"
        )
        sys.exit(1)

    # Inicializar cliente DeepSeek
    client = openai.OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )

    # Preparar el prompt inicial
    prompt_completo = AGENT_PROMPT.replace("{{pedido_usuario}}", args.prompt)
    messages = [{"role": "user", "content": prompt_completo}]

    iteraciones = 0

    console.print(Panel(f"[bold green]🚀 Iniciando Agente PostgreSQL con DeepSeek[/bold green]\nPedido: {args.prompt}", title="SFA PostgreSQL"))

    # Loop agéntico principal
    while True:
        console.rule(
            f"[yellow]Iteración {iteraciones+1}/{args.compute}[/yellow]"
        )
        iteraciones += 1

        if iteraciones >= args.compute:
            console.print(
                "[yellow]⚠️ Alcanzado el máximo de iteraciones sin consulta final[/yellow]"
            )
            break

        try:
            # Llamar a DeepSeek API
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=messages,
                tools=tools,
                tool_choice="required"
            )

            if response.choices:
                message = response.choices[0].message

                # Procesar tool calls
                if message.tool_calls:
                    tool_call = message.tool_calls[0]
                    func_name = tool_call.function.name
                    func_args_str = tool_call.function.arguments

                    # Agregar respuesta del asistente a los mensajes
                    messages.append({
                        "role": "assistant",
                        "tool_calls": [{
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": func_name,
                                "arguments": func_args_str
                            }
                        }]
                    })

                    console.print(
                        f"[blue]🔧 Llamada a Herramienta:[/blue] {func_name}"
                    )

                    try:
                        # Parsear y ejecutar la herramienta correspondiente
                        if func_name == "ListarTablasArgs":
                            args_parsed = ListarTablasArgs.model_validate_json(func_args_str)
                            result = listar_tablas(razonamiento=args_parsed.razonamiento)

                        elif func_name == "DescribirTablaArgs":
                            args_parsed = DescribirTablaArgs.model_validate_json(func_args_str)
                            result = describir_tabla(
                                razonamiento=args_parsed.razonamiento,
                                nombre_tabla=args_parsed.nombre_tabla
                            )

                        elif func_name == "MuestrearTablaArgs":
                            args_parsed = MuestrearTablaArgs.model_validate_json(func_args_str)
                            result = muestrear_tabla(
                                razonamiento=args_parsed.razonamiento,
                                nombre_tabla=args_parsed.nombre_tabla,
                                cantidad_filas=args_parsed.cantidad_filas
                            )

                        elif func_name == "ListarRelacionesArgs":
                            args_parsed = ListarRelacionesArgs.model_validate_json(func_args_str)
                            result = listar_relaciones(
                                razonamiento=args_parsed.razonamiento,
                                nombre_tabla=args_parsed.nombre_tabla
                            )

                        elif func_name == "EjecutarConsultaPruebaArgs":
                            args_parsed = EjecutarConsultaPruebaArgs.model_validate_json(func_args_str)
                            result = ejecutar_consulta_prueba(
                                razonamiento=args_parsed.razonamiento,
                                consulta_sql=args_parsed.consulta_sql
                            )

                        elif func_name == "EjecutarConsultaFinalArgs":
                            args_parsed = EjecutarConsultaFinalArgs.model_validate_json(func_args_str)
                            result = ejecutar_consulta_final(
                                razonamiento=args_parsed.razonamiento,
                                consulta_sql=args_parsed.consulta_sql
                            )
                            console.print("\n[green]✅ Resultados Finales:[/green]")
                            return

                        else:
                            raise Exception(f"Herramienta desconocida: {func_name}")

                        # Agregar resultado de la herramienta a los mensajes
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"result": str(result)}, ensure_ascii=False)
                        })

                    except ValidationError as e:
                        error_msg = f"Error de validación para {func_name}: {e}"
                        console.print(f"[red]{error_msg}[/red]")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"error": error_msg}, ensure_ascii=False)
                        })
                        continue

                else:
                    console.print("[yellow]No se recibieron llamadas a herramientas[/yellow]")
                    break

        except Exception as e:
            console.print(f"[red]Error en el loop del agente: {str(e)}[/red]")
            break

    console.print("[bold red]❌ El agente finalizó sin completar la tarea[/bold red]")


if __name__ == "__main__":
    main()
