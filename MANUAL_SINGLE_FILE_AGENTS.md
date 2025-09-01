# Manual Completo de Single File Agents (SFA)

## 📚 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Arquitectura Core](#arquitectura-core)
3. [Anatomía de un SFA](#anatomía-de-un-sfa)
4. [Patrones de Diseño](#patrones-de-diseño)
5. [Function Calling / Tool Use](#function-calling--tool-use)
6. [Compatibilidad con DeepSeek](#compatibilidad-con-deepseek)
7. [Guía Paso a Paso](#guía-paso-a-paso)
8. [Mejores Prácticas](#mejores-prácticas)

---

## Introducción

Los **Single File Agents (SFA)** son una arquitectura revolucionaria que empaqueta agentes de IA completos y funcionales en un único archivo Python. Esta filosofía minimalista aprovecha `uv` (el gestor de paquetes moderno de Python) para crear agentes portables, autocontenidos y fáciles de ejecutar.

### ¿Por qué Single File Agents?

- **Simplicidad**: Un archivo = Una funcionalidad completa
- **Portabilidad**: Ejecutable desde cualquier lugar con `uv run`
- **Autocontenido**: Dependencias embebidas en el archivo
- **Mantenibilidad**: Fácil de entender, modificar y compartir
- **Escalabilidad**: La inteligencia crece con el modelo, no con el código

---

## Arquitectura Core

### 1. Sistema de Dependencias con UV

```python
# /// script
# dependencies = [
#   "openai>=1.63.0",
#   "rich>=13.7.0",
#   "pydantic>=2.0.0",
# ]
# ///
```

Este bloque mágico al inicio del archivo le dice a `uv` qué dependencias instalar automáticamente. No necesitas `requirements.txt` ni entornos virtuales manuales.

### 2. Estructura Base de un SFA

```python
#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [...]
# ///

"""Documentación y ejemplos de uso"""

import os
import sys
import argparse
# ... más imports

# Configuración de prompts
AGENT_PROMPT = """<purpose>...</purpose>"""

# Definición de herramientas/funciones
class ToolArgs(BaseModel):
    reasoning: str = Field(...)
    # ... más campos

# Funciones de herramientas
def tool_function(args):
    # Implementación
    pass

# Función principal
def main():
    parser = argparse.ArgumentParser()
    # Configuración de argumentos
    args = parser.parse_args()
    
    # Verificación de API keys
    API_KEY = os.getenv("PROVIDER_API_KEY")
    
    # Loop principal del agente
    # ...

if __name__ == "__main__":
    main()
```

---

## Anatomía de un SFA

### Componentes Esenciales

#### 1. **Bloque de Dependencias**
```python
# /// script
# dependencies = [
#   "google-genai>=1.1.0",  # Para Gemini
#   "openai>=1.63.0",       # Para OpenAI
#   "anthropic>=0.45.2",    # Para Claude
# ]
# ///
```

#### 2. **Sistema de Prompts Estructurados**
```python
AGENT_PROMPT = """<purpose>
    Define claramente qué hace el agente
</purpose>

<instructions>
    <instruction>Paso a paso de cómo debe comportarse</instruction>
    <instruction>Reglas específicas del dominio</instruction>
</instructions>

<examples>
    <example>
        <user-request>Ejemplo de entrada</user-request>
        <expected-output>Ejemplo de salida</expected-output>
    </example>
</examples>

<user-request>
    {{user_request}}  # Placeholder para input del usuario
</user-request>"""
```

#### 3. **Definición de Herramientas con Pydantic**
```python
class ListTablesArgs(BaseModel):
    reasoning: str = Field(
        ..., 
        description="Explicación del por qué se llama esta herramienta"
    )
    database_path: str = Field(
        ..., 
        description="Ruta a la base de datos"
    )
```

#### 4. **Implementación de Herramientas**
```python
def list_tables(reasoning: str, database_path: str) -> List[str]:
    """Lista las tablas en una base de datos.
    
    Args:
        reasoning: Por qué necesitamos listar las tablas
        database_path: Ruta a la base de datos
        
    Returns:
        Lista de nombres de tablas
    """
    try:
        # Ejecutar comando o lógica
        result = subprocess.run(...)
        return process_result(result)
    except Exception as e:
        console.log(f"[red]Error: {e}[/red]")
        return []
```

#### 5. **Loop de Compute Iterativo**
```python
def main():
    compute_iterations = 0
    max_compute = args.compute or 10
    
    while compute_iterations < max_compute:
        compute_iterations += 1
        
        # Llamada a la API del modelo
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="required"
        )
        
        # Procesar respuesta y ejecutar herramientas
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            result = execute_tool(tool_call)
            
            # Si es resultado final, terminar
            if is_final_result(result):
                return result
                
        # Agregar resultado a la conversación
        messages.append({"role": "tool", "content": result})
```

---

## Patrones de Diseño

### 1. **Patrón de Herramientas Progresivas**

Los agentes siguen un flujo de exploración → prueba → ejecución:

```python
tools = [
    # Exploración
    pydantic_function_tool(ListTablesArgs),      # Descubrimiento
    pydantic_function_tool(DescribeTableArgs),   # Esquema
    pydantic_function_tool(SampleTableArgs),     # Datos ejemplo
    
    # Prueba
    pydantic_function_tool(RunTestQueryArgs),    # Validación
    
    # Ejecución
    pydantic_function_tool(RunFinalQueryArgs),   # Resultado final
]
```

### 2. **Patrón de Reasoning Obligatorio**

Cada herramienta SIEMPRE incluye un campo `reasoning`:

```python
class ToolArgs(BaseModel):
    reasoning: str = Field(
        ..., 
        description="Explicación del por qué esta acción"
    )
    # ... otros campos
```

Esto fuerza al modelo a "pensar" antes de actuar.

### 3. **Patrón de Salida Rica**

Uso de `rich` para feedback visual:

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# Feedback estructurado
console.rule("[yellow]Iteración {}/{}[/yellow]".format(i, max))
console.log("[blue]Ejecutando herramienta[/blue]")
console.print(Panel("Resultado final", style="green"))
```

---

## Function Calling / Tool Use

### OpenAI Style
```python
# Definir herramientas con Pydantic
tools = [pydantic_function_tool(MyToolArgs)]

# Llamar al modelo con herramientas
response = openai.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=tools,
    tool_choice="required"  # Forzar uso de herramientas
)

# Procesar llamada a herramienta
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)
    
    # Ejecutar herramienta
    result = my_tool_function(**func_args)
```

### Anthropic Style
```python
# Definir herramientas
tools = [
    {
        "name": "view_file",
        "description": "Ver contenido de un archivo",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "reasoning": {"type": "string"}
            },
            "required": ["path", "reasoning"]
        }
    }
]

# Llamar a Claude con herramientas
response = client.messages.create(
    model="claude-3-sonnet",
    messages=messages,
    tools=tools,
    tool_choice={"type": "any"}
)

# Procesar uso de herramientas
for content_block in response.content:
    if content_block.type == "tool_use":
        tool_name = content_block.name
        tool_input = content_block.input
        result = execute_tool(tool_name, tool_input)
```

### Gemini Style
```python
# Gemini usa un enfoque más directo
prompt = AGENT_PROMPT.replace("{{user_request}}", user_input)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

# El resultado viene como texto que luego se ejecuta
command = response.text.strip()
subprocess.run(command, shell=True)
```

---

## Compatibilidad con DeepSeek

DeepSeek ofrece compatibilidad con la API de OpenAI, lo que significa que **SÍ puedes usar los SFA con DeepSeek** con mínimas modificaciones:

### Configuración para DeepSeek

```python
import openai

# Configurar cliente para DeepSeek
client = openai.OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"  # URL de DeepSeek
)

# Usar modelos DeepSeek
response = client.chat.completions.create(
    model="deepseek-chat",  # o "deepseek-reasoner"
    messages=messages,
    tools=tools,  # Soporta function calling
    tool_choice="auto"
)
```

### Consideraciones para DeepSeek

1. **Modelos Disponibles**:
   - `deepseek-chat`: Modo no-razonamiento de DeepSeek-V3
   - `deepseek-reasoner`: Modo con razonamiento

2. **Limitaciones Conocidas**:
   - Function calling multi-turno puede ser inestable
   - Mejor rendimiento en llamadas single-turn
   - DeepSeek-R1 aún no soporta function calling completamente

3. **Modificación Mínima de SFA Existente**:

```python
# Original (OpenAI)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modificado para DeepSeek
client = openai.OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# El resto del código permanece igual
```

---

## Guía Paso a Paso

### Paso 1: Preparar el Entorno

```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Configurar API keys
export DEEPSEEK_API_KEY='tu-api-key'
export OPENAI_API_KEY='tu-api-key'
export ANTHROPIC_API_KEY='tu-api-key'
```

### Paso 2: Crear tu Primer SFA

```python
#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "openai>=1.63.0",
#   "rich>=13.7.0",
# ]
# ///

"""
Mi primer Single File Agent
Uso: uv run mi_agente.py --prompt "Tu pregunta aquí"
"""

import os
import sys
import argparse
from rich.console import Console
import openai

console = Console()

PROMPT_TEMPLATE = """Eres un asistente útil.
Usuario: {user_input}
Respuesta:"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()
    
    # Para DeepSeek
    client = openai.OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": PROMPT_TEMPLATE.format(
                user_input=args.prompt
            )}
        ]
    )
    
    console.print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

### Paso 3: Ejecutar el Agente

```bash
uv run mi_agente.py --prompt "Explica qué es un SFA"
```

### Paso 4: Añadir Herramientas

```python
from pydantic import BaseModel, Field
from openai import pydantic_function_tool

class CalculatorArgs(BaseModel):
    reasoning: str = Field(..., description="Por qué calcular esto")
    expression: str = Field(..., description="Expresión matemática")

def calculator(reasoning: str, expression: str) -> str:
    console.log(f"[blue]Calculando:[/blue] {expression}")
    console.log(f"[dim]Razón: {reasoning}[/dim]")
    try:
        result = eval(expression)  # Solo para demo, usar con cuidado
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# En main():
tools = [pydantic_function_tool(CalculatorArgs)]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

---

## Mejores Prácticas

### 1. **Estructura Clara de Prompts**
- Usa etiquetas XML para organizar: `<purpose>`, `<instructions>`, `<examples>`
- Incluye ejemplos concretos
- Define claramente los límites y capacidades

### 2. **Manejo de Errores Robusto**
```python
try:
    result = execute_operation()
except SpecificError as e:
    console.log(f"[yellow]Advertencia: {e}[/yellow]")
    # Intentar recuperación
except Exception as e:
    console.log(f"[red]Error crítico: {e}[/red]")
    sys.exit(1)
```

### 3. **Límites de Compute**
```python
MAX_ITERATIONS = 10  # Evitar loops infinitos
if iterations >= MAX_ITERATIONS:
    console.print("[yellow]Alcanzado límite de iteraciones[/yellow]")
    return best_result_so_far
```

### 4. **Validación de Entradas**
```python
# Siempre validar API keys
if not os.getenv("DEEPSEEK_API_KEY"):
    console.print("[red]Error: DEEPSEEK_API_KEY no configurada[/red]")
    console.print("Configura con: export DEEPSEEK_API_KEY='tu-key'")
    sys.exit(1)

# Validar archivos/rutas
if not os.path.exists(args.file):
    console.print(f"[red]Archivo no encontrado: {args.file}[/red]")
    sys.exit(1)
```

### 5. **Documentación Inline**
```python
"""
Ejemplo de uso:
    # Básico
    uv run agente.py --prompt "consulta"
    
    # Con opciones
    uv run agente.py --prompt "consulta" --compute 5 --output resultado.txt
"""
```

### 6. **Herramientas Atómicas**
Cada herramienta debe hacer UNA cosa bien:
- ❌ `process_and_save_data()`
- ✅ `process_data()` + `save_result()`

### 7. **Feedback Visual**
```python
# Usar rich para mejor UX
console.rule("[bold blue]Iniciando Agente[/bold blue]")
with console.status("[bold green]Procesando..."):
    result = long_operation()
console.print(Panel(result, title="Resultado", style="green"))
```

---

## Conclusión

Los Single File Agents representan un paradigma elegante y poderoso para crear agentes de IA. Su arquitectura minimalista no sacrifica funcionalidad, y su compatibilidad con múltiples proveedores (incluyendo DeepSeek) los hace versátiles y accesibles.

**Ventajas clave con DeepSeek:**
- ✅ Compatibilidad OpenAI API
- ✅ Soporte de function calling
- ✅ Costos potencialmente menores
- ✅ Modelos potentes y especializados

**Recuerda:**
1. Un archivo, una responsabilidad
2. Dependencias embebidas con `uv`
3. Herramientas progresivas (explorar → probar → ejecutar)
4. Siempre incluir reasoning en las herramientas
5. Límites de compute para evitar loops infinitos
6. Feedback visual rico para mejor UX

Con este conocimiento, estás listo para crear tus propios Single File Agents potentes, portables y mantenibles. ¡Adelante!