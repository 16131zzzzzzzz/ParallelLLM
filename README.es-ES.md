# Parallel LLM Client Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

Un marco de trabajo para la invocación paralela de Modelos de Lenguaje Extensos (LLM) que proporciona:

- Balanceo de carga entre múltiples proveedores de LLM
- Interfaces híbridas síncronas/asíncronas
- Failover automático y mecanismos inteligentes de reintento

## Inicio Rápido

### Instalación

```bash
git clone https://github.com/16131zzzzzzzz/ParallelLLM.git
cd ParallelLLM
pip install -r requirements.txt
pip install -e .
```

### Configuración

1. Modifique el archivo de configuración: `examples/example_config.yaml`

```yaml
llm:
  use: siliconflow
  siliconflow:
    - api_key: 'sk-xxx'
      api_base: 'https://api.siliconflow.cn/v1/chat/completions'
      model: 'model name'
      rate_limit: 20

    - api_key: 'sk-xxx'
      api_base: 'https://api.siliconflow.cn/v1/chat/completions'
      model: 'model name'
      rate_limit: 20
```

### Ejemplos de Uso

#### 1. Inicializar Cliente

```python
from pllm import Client

client = Client("examples/example_config.yaml")
```

#### 2. Métodos Síncronos Comunes

##### 2.1 Generación de Texto - `invoke()` / `generate_sync()`

Generar texto a partir de un único prompt:

```python
response = client.invoke(
    "写一个快速排序算法的Python实现",
    retry_policy="retry_once",
    temperature=0.3
)
print(response)

# Método alternativo (funcionalidad idéntica)
response = client.generate_sync(
    "写一个正则表达式匹配邮箱地址",
    retry_policy="infinite"
)
print(response)
```

##### 2.2 Procesamiento por Lotes - `invoke_batch()`

Procesar múltiples prompts en paralelo:

```python
questions = [
    "解释量子隧穿效应",
    "写一个快速排序算法",
    "什么是Transformer架构？",
    "如何用Python计算圆周率？",
    "解释深度神经网络的工作原理"
]

results = client.invoke_batch(
    questions,
    retry_policy="fixed",
    temperature=0.6
)

for i, result in enumerate(results):
    print(f"Question {i+1}: {questions[i]}")
    print(f"Answer: {result}\n")
```

##### 2.3 Embeddings de Texto - `embedding_sync()`

Generar embeddings de texto para similitud vectorial:

```python
embedding = client.embedding_sync(
    "计算这段文本的向量表示",
    encoding_format="float"
)
print(f"Embedding length: {len(embedding)}")
```

#### 3. Estadísticas de Uso

Monitorear el uso de la API en todos los proveedores:

```python
stats = client.get_stats()
print("Usage Statistics:")
for provider, clients in stats.items():
    print(f"\nProvider: {provider}")
    for client_info in clients:
        print(f"  Client {client_info['id']}:")
        print(f"    Active: {client_info['active']}")
        print(f"    Total Requests: {client_info['total_requests']}")
        print(f"    Total Tokens: {client_info['total_tokens']}")
        print(f"    Error Count: {client_info['error_count']}")
```

## Uso Avanzado

### Métodos Asíncronos

#### Generación de Texto - `generate()`

```python
import asyncio

async def example_generate():
    response = await client.generate(
        "解释一下量子计算的基本原理",
        retry_policy="infinite",
        temperature=0.5
    )
    print(response)

asyncio.run(example_generate())
```

#### Embeddings de Texto - `embedding()`

```python
async def example_embedding():
    embedding = await client.embedding(
        "这是一段需要向量化的文本",
        encoding_format="float",
        retry_policy="fixed"
    )
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")

asyncio.run(example_embedding())
```

### Procesamiento Paralelo

Procesar múltiples solicitudes simultáneamente:

```python
async def parallel_processing():
    tasks = [
        client.generate("什么是机器学习？"),
        client.generate("解释深度学习原理"),
        client.generate("什么是自然语言处理？"),
        client.embedding("向量化这段文本")
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

results = asyncio.run(parallel_processing())
```

### Manejo de Errores con Políticas de Reintento

```python
# Reintento infinito hasta el éxito
response = await client.generate(
    "重要的请求，必须成功",
    retry_policy="infinite"
)

# Número fijo de reintentos
response = await client.generate(
    "普通请求",
    retry_policy="fixed"
)

# Reintentar solo una vez
response = await client.generate(
    "简单请求",
    retry_policy="retry_once"
)
```

### Solicitudes Específicas de Proveedor

```python
# Forzar el uso de un proveedor específico
response = await client.generate(
    "Hello",
    provider="siliconflow"
)
```

## Pruebas

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas unitarias (nueva suite de pruebas exhaustiva)
python tests/run_tests.py --unit

# Ejecutar pruebas del algoritmo de balanceo (selección de proveedor, conteo de tokens, failover)
python -m unittest tests.test_balance_algorithm -v

# Ejecutar pruebas de la interfaz del cliente (invoke, invoke_batch, chat, generate, etc.)
python -m unittest tests.test_client_interface -v

# Ejecutar pruebas de integración (requiere claves de API reales)
python tests/run_tests.py --integration

# Ejecutar pruebas de proveedor (pruebas mock para todos los proveedores)
python tests/run_tests.py --provider all

# Ejecutar pruebas de un proveedor específico
python tests/run_tests.py --provider openai

# Ejecutar todas las pruebas
python tests/run_tests.py --all
```

### Pruebas Manuales

```bash
# Pruebas manuales con llamadas API reales (requiere claves API válidas)
python tests/manual_test.py
python tests/multi_key_test.py
```

## TODO

- [ ] Actualmente solo soporta siliconflow, es necesario agregar más proveedores de LLM
- [ ] Cambiar los comentarios a inglés
