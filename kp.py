import os
import time

def parse_file(file_path):
    """
    Parse o arquivo para extrair a capacidade e itens.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Verifique se o arquivo possui pelo menos uma linha
        if len(lines) < 2:
            raise ValueError(f"Arquivo {file_path} não contém linhas suficientes.")

        # Primeira linha contém quantidade de itens e capacidade
        num_items, capacity = map(int, lines[0].strip().split())

        # Verifique se o arquivo tem linhas suficientes para os itens
        if len(lines) < num_items + 1:
            raise ValueError(f"Arquivo {file_path} contém {len(lines)} linhas, mas são esperadas {num_items + 1} linhas.")

        # Próximas linhas contêm valor e peso dos itens
        items = [tuple(map(int, line.strip().split())) for line in lines[1:num_items + 1]]

        return capacity, items
    except Exception as e:
        print(f"Erro ao analisar o arquivo {file_path}: {e}")
        return None, None

def greedy_smallest_weight(capacity, items):
    """
    Algoritmo guloso que seleciona os itens com menor peso.
    """
    items_sorted = sorted(items, key=lambda x: x[1])
    total_value = total_weight = 0
    for value, weight in items_sorted:
        if total_weight + weight <= capacity:
            total_value += value
            total_weight += weight
        else:
            break
    return total_value

def greedy_best_ratio(capacity, items):
    """
    Algoritmo guloso que seleciona itens com melhor relação valor/peso.
    """
    items_sorted = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    total_value = total_weight = 0
    for value, weight in items_sorted:
        if total_weight + weight <= capacity:
            total_value += value
            total_weight += weight
        else:
            break
    return total_value

def knapsack_dynamic_programming(capacity, items):
    """
    Algoritmo de programação dinâmica para o problema da mochila.
    """
    n = len(items)
    dp = [0] * (capacity + 1)
    for value, weight in items:
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[capacity]

def evaluate_file(file_path, optimal_value):
    """
    Avalia o arquivo com as três abordagens e calcula a qualidade das soluções.
    """
    capacity, items = parse_file(file_path)

    if capacity is None or items is None:
        return None

    start_time = time.perf_counter()
    greedy_1_value = greedy_smallest_weight(capacity, items)
    greedy_1_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    greedy_2_value = greedy_best_ratio(capacity, items)
    greedy_2_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    dp_value = knapsack_dynamic_programming(capacity, items)
    dp_time = time.perf_counter() - start_time

    quality_greedy_1 = greedy_1_value / optimal_value
    quality_greedy_2 = greedy_2_value / optimal_value
    quality_dp = dp_value / optimal_value

    return {
        "greedy_1_value": greedy_1_value, "greedy_1_time": greedy_1_time, "quality_greedy_1": quality_greedy_1,
        "greedy_2_value": greedy_2_value, "greedy_2_time": greedy_2_time, "quality_greedy_2": quality_greedy_2,
        "dp_value": dp_value, "dp_time": dp_time, "quality_dp": quality_dp
    }

def process_directory(directory, optimum_values):
    """
    Processa todos os arquivos no diretório e retorna os resultados.
    """
    results = []
    file_names = []
    for file_name in sorted(os.listdir(directory)):
        if file_name in optimum_values:
            file_path = os.path.join(directory, file_name)
            optimal_value = optimum_values[file_name]
            result = evaluate_file(file_path, optimal_value)
            if result is not None:
                results.append(result)
                file_names.append(file_name)
    return results, file_names

def display_results(results, file_names):
    """
    Exibe os resultados das avaliações no terminal.
    """
    if not results:
        print("Nenhum resultado para exibir.")
        return

    # Cabeçalhos
    print(f"{'Arquivo':<30} {'Algoritmo':<25} {'Tempo (s)':<15} {'Qualidade da Solução'}")
    print("=" * 80)

    for i, result in enumerate(results):
        file_name = file_names[i]
        
        # Exibindo os resultados para o algoritmo guloso 1 (menor peso)
        print(f"{file_name:<30} {'Greedy Smallest Weight':<25} {result['greedy_1_time']:<15.6f} {result['quality_greedy_1']:.6f}")

        # Exibindo os resultados para o algoritmo guloso 2 (melhor razão valor/peso)
        print(f"{file_name:<30} {'Greedy Best Ratio':<25} {result['greedy_2_time']:<15.6f} {result['quality_greedy_2']:.6f}")

        # Exibindo os resultados para o algoritmo de programação dinâmica
        print(f"{file_name:<30} {'Dynamic Programming':<25} {result['dp_time']:<15.6f} {result['quality_dp']:.6f}")

    print("=" * 80)

if __name__ == "__main__":
    directory = "/home/farrapo/large_scale/"
    optimum_values = {
        "knapPI_1_100_1000_1": 9147,
        "knapPI_1_200_1000_1": 11238,
        "knapPI_1_500_1000_1": 28857,
        "knapPI_1_1000_1000_1": 54503,
        "knapPI_1_2000_1000_1": 110625,
        "knapPI_1_5000_1000_1": 276457,
        "knapPI_1_10000_1000_1": 563647,
        "knapPI_2_100_1000_1": 1514,
        "knapPI_2_200_1000_1": 1634,
        "knapPI_2_500_1000_1": 4566,
        "knapPI_2_1000_1000_1": 9052,
        "knapPI_2_2000_1000_1": 18051,
        "knapPI_2_5000_1000_1": 44356,
        "knapPI_2_10000_1000_1": 90204,
        "knapPI_3_100_1000_1": 2397,
        "knapPI_3_200_1000_1": 2697,
        "knapPI_3_500_1000_1": 7117,
        "knapPI_3_1000_1000_1": 14390,
        "knapPI_3_2000_1000_1": 28919,
        "knapPI_3_5000_1000_1": 72505,
        "knapPI_3_10000_1000_1": 146919
    }

    results, file_names = process_directory(directory, optimum_values)
    display_results(results, file_names)

