import pandas as pd
import re
import time

def CleanDistance(distance):
    return int(re.sub(r'[^\d]', '', distance))

def CleanPrice(price):
    price = price.lower().replace('pkr', '').strip()
    try:
        if 'crore' in price:
            return float(price.replace('crore', '').strip()) * 100  # Convert crore to lacs
        elif 'lacs' in price or 'lac' in price:
            return float(price.replace('lacs', '').replace('lac', '').strip())  
        return float(price)
    except ValueError:
        return 0.0 


def CleanEngine(engine):
    if 'cc' in engine:
        return float(engine.replace('cc', '').strip())
    elif 'kwh' in engine.lower():
        return float(engine.lower().replace('kwh', '').strip()) * 1000  # Convert kWh to cc equivalent
    return 1.0  #handle float values

def RestoreDistance(distance):
    return f"{distance} km"

def RestorePrice(price):
    if price == 0:
        return 'call'  # Restore invalid price as 'call'
    if price >= 100:
        return f"PKR {price / 100} crore"
    else:
        return f"PKR {price} lacs"

def RestoreEngine(engine):
    if engine >= 1000:
        return f"{engine / 1000} kWh"
    else:
        return f"{engine} cc"

# Sorting Algorithms
def BubbleSort(data, column, start, end):
    dataf = data.iloc[start:end + 1].copy()
    n = len(dataf)
    swapped = False
    for i in range(n):
        for j in range(n-i- 1):
            if dataf.iloc[j][column] > dataf.iloc[j + 1][column]:
                dataf.iloc[j], dataf.iloc[j + 1] = dataf.iloc[j + 1].copy(), dataf.iloc[j].copy()
                swapped = True
        if(not swapped):
            break
    data.iloc[start:end + 1] = dataf
    return data

def SelectionSort(data, column, start, end):
    dataf = data.iloc[start:end + 1].copy()
    n = len(dataf)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if dataf.iloc[j][column] < dataf.iloc[min_index][column]:
                min_index = j
        dataf.iloc[[min_index, i]] = dataf.iloc[[i, min_index]].values
    data.iloc[start:end + 1] = dataf
    return data

def InsertionSort(data, column, start, end):
    dataf = data.iloc[start:end + 1].copy()
    n = len(dataf)
    for i in range(1, n):
        key = dataf.iloc[i]
        j = i - 1
        while j >= 0 and key[column] < dataf.iloc[j][column]:
            dataf.iloc[j + 1] = dataf.iloc[j]
            j -= 1
        dataf.iloc[j + 1] = key
    data.iloc[start:end + 1] = dataf
    return data

def MergeSort(data, column, start, end):
    if start < end:
        mid = (start + end) // 2
        MergeSort(data, column, start, mid)
        MergeSort(data, column, mid + 1, end)
        Merge(data, column, start, mid, end)
    return data

def Merge(data, column, start, mid, end):
    left = data.iloc[start:mid + 1].copy()
    right = data.iloc[mid + 1:end + 1].copy()
    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        if left.iloc[i][column] <= right.iloc[j][column]:
            data.iloc[k] = left.iloc[i]
            i += 1
        else:
            data.iloc[k] = right.iloc[j]
            j += 1
        k += 1

    while i < len(left):
        data.iloc[k] = left.iloc[i]
        i += 1
        k += 1

    while j < len(right):
        data.iloc[k] = right.iloc[j]
        j += 1
        k += 1

def QuickSort(data, column, start, end):
    if start < end:
        pi = Partition(data, column, start, end)
        QuickSort(data, column, start, pi - 1)
        QuickSort(data, column, pi + 1, end)
    return data    

def Partition(data, column, start, end):
    pivot = data.iloc[end][column]
    i = start - 1
    for j in range(start, end):
        if data.iloc[j][column] < pivot:
            i += 1
            data.iloc[[i, j]] = data.iloc[[j, i]].values
    data.iloc[[i + 1, end]] = data.iloc[[end, i + 1]].values
    return i + 1

def HeapSort(data, column, start, end):
    n = end - start + 1

    for i in range(n // 2 - 1, -1, -1):
        Heapify(data, column, n, i, start)

    for i in range(n - 1, 0, -1):
        data.iloc[start], data.iloc[start + i] = data.iloc[start + i].copy(), data.iloc[start].copy()
        Heapify(data, column, i, 0, start)
    return data

def Heapify(data, column, n, i, start):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and data.iloc[start + left][column] > data.iloc[start + largest][column]:
        largest = left

    if right < n and data.iloc[start + right][column] > data.iloc[start + largest][column]:
        largest = right

    if largest != i:
        data.iloc[start + i], data.iloc[start + largest] = data.iloc[start + largest].copy(), data.iloc[start + i].copy()
        Heapify(data, column, n, largest, start)

def HybridMergeSort(data, column, start, end):
    if end - start <= 10:
        InsertionSort(data, column, start, end)
    else:
        MergeSort(data, column, start, end)
    return data

def ShellSort(data, column, start, end):
    n = end - start + 1
    gap = n // 2

    while gap > 0:
        for i in range(start + gap, end + 1):
            temp = data.iloc[i].copy()  
            j = i
            while j >= start + gap and data.iloc[j - gap][column] > temp[column]:
                data.iloc[j] = data.iloc[j - gap]  # Shift the row
                j -= gap
            data.iloc[j] = temp  
        gap //= 2
    return data
    
def CountingSort(data, column, start, end):
    max_value = int(data.iloc[start:end + 1][column].max()) + 1
    count = [0] * max_value
    output = [0] * (end - start + 1)

    for i in range(start, end + 1):
        j = int(data.iloc[i][column])
        count[j] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(end, start - 1, -1):
        output[count[int(data.iloc[i][column])] - 1] = data.iloc[i]
        count[int(data.iloc[i][column])] -= 1

    for i in range(len(output)):
        data.iloc[start + i] = output[i]

    return data

def RadixSort(data, column, start, end):
    max_num = int(data[column].max())
    exp = 1

    while max_num // exp > 0:
        CountingSortRadix(data, column, start, end, exp)
        exp *= 10
    return data    

def CountingSortRadix(data, column, start, end, exp):
    output = [0] * (end - start + 1)
    count = [0] * 10

    for i in range(start, end + 1):
        index = (int(data.iloc[i][column]) // exp) % 10
        count[index] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(end, start - 1, -1):
        index = (int(data.iloc[i][column]) // exp) % 10
        output[count[index] - 1] = data.iloc[i]
        count[index] -= 1

    for i in range(len(output)):
        data.iloc[start + i] = output[i]

def BucketSort(data, column, start, end):
    max_value = data[column].max()
    min_value = data[column].min()  
    range_value = max_value - min_value
    size = range_value / (end - start + 1)
    
    buckets = [[] for _ in range(end - start + 1)]
    for i in range(start, end + 1):
        index = int((data.iloc[i][column] - min_value) / size)
        
        if index == end - start + 1:
            index = end - start
        
        buckets[index].append(data.iloc[i])
    output = []
    for bucket in buckets:
        if bucket:
            output.extend(sorted(bucket, key=lambda x: x[column]))
    for i in range(len(output)):
        data.iloc[start + i] = output[i]
    
    return data


def PigeonholeSort(data, column, start, end):
    min_value = int(data.iloc[start:end + 1][column].min())
    max_value = int(data.iloc[start:end + 1][column].max())
    size = max_value - min_value + 1
    holes = [[] for _ in range(size)]

    for i in range(start, end + 1):
        holes[int(data.iloc[i][column]) - min_value].append(data.iloc[i])

    output = []
    for hole in holes:
        if hole:
            output.extend(hole)

    for i in range(len(output)):
        data.iloc[start + i] = output[i]
    return data
 
def ApplySorting(data, column, sort_type):
    #original_values = data[column].copy()
    
    # Clean the data for numerical sorting
    if column == 'Mileage':
        data[column] = data[column].apply(CleanDistance)
    elif column == 'Price':
        data[column] = data[column].apply(CleanPrice)
    elif column == 'Engine':
        data[column] = data[column].apply(CleanEngine)

    start = 0
    end = len(data)-1
    
    
    # start_time = time.time()

    if sort_type == 'Bubble Sort':
        data = BubbleSort(data, column, start, end)
    elif sort_type == 'Selection Sort':
        data = SelectionSort(data, column, start, end)
    elif sort_type == 'Insertion Sort':
        data = InsertionSort(data, column, start, end)
    elif sort_type == 'Merge Sort':
        data = MergeSort(data, column, start, end)
    elif sort_type == 'Quick Sort':
        data = QuickSort(data, column, start, end)
    elif sort_type == 'Heap Sort':
        data = HeapSort(data, column, start, end)
    elif sort_type == 'Hybrid Merge Sort':
        data = HybridMergeSort(data, column, start, end)
    elif sort_type == 'Shell Sort':
        data = ShellSort(data, column, start, end)
    elif sort_type == 'Counting Sort':
        data = CountingSort(data, column, start, end)
    elif sort_type == 'Radix Sort':
        data = RadixSort(data, column, start, end)
    elif sort_type == 'Bucket Sort':
        data = BucketSort(data, column, start, end)
    elif sort_type == 'Pigeonhole Sort':
        data = PigeonholeSort(data, column, start, end)


    # end_time = time.time()
    # sorting_time = (end_time - start_time) * 1000  # Convert to milliseconds

    # Restoring the original formats after sorting
    if column == 'Mileage':
        data[column] = data[column].apply(RestoreDistance)
    elif column == 'Price':
        data[column] = data[column].apply(RestorePrice)
    elif column == 'Engine':
        data[column] = data[column].apply(RestoreEngine)


    return data
    # For checking 
    # data.to_csv('sorted_data.csv', index=False)
    # print(f"Data sorted by {column} using {sort_type} sort in ms and saved to 'sorted_data.csv'.")

def readf(file):
    data = pd.read_csv(file)
    return data


if __name__ == "__main__":
    
    data = readf('data.csv')
    allowed_columns = ['Title','Transmission','Model', 'Price', 'Mileage', 'Engine','Fuel Type']
    column_to_sort = 'Price'  
    sorting_algorithm = 'Radix Sort'  
    
    if column_to_sort in allowed_columns:
        ApplySorting(data, column_to_sort, sorting_algorithm)
    else:
        print(f"Column '{column_to_sort}' is not allowed. Choose from {allowed_columns}.")
