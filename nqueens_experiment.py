import time
from ortools.sat.python import cp_model

def run_nqueens_benchmark():
    results = []
    print("N  | Method  | Status      | Time (s)")
    print("-" * 40)
    
    # Danh sách các kích thước N cần chạy thực nghiệm (từ nhỏ đến lớn)
    test_sizes = [8, 12, 16, 20, 24, 30]
    
    for N in test_sizes:
        start_time = time.time()
        model = cp_model.CpModel()
        
        # Biến đại diện cho vị trí cột của quân hậu ở mỗi hàng
        x = [model.NewIntVar(0, N - 1, f'x_{i}') for i in range(N)]
        
        # Ràng buộc N-Queens: Khác cột, khác đường chéo chính và chéo phụ
        model.AddAllDifferent(x)
        model.AddAllDifferent([x[i] + i for i in range(N)])
        model.AddAllDifferent([x[i] - i for i in range(N)])
        
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        elapsed = time.time() - start_time
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            status_str = "SAT"
        else:
            status_str = "UNSAT"
            
        results.append(f"{N},CP-SAT,{status_str},{elapsed:.4f}")
        print(f"{N:<2} | CP-SAT  | {status_str:<11} | {elapsed:.4f}")

    # Tự động xuất số liệu ra file CSV dạng bảng
    filename = "nqueens_benchmark_results.csv"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("N,Method,Status,Time_Seconds\n")
        f.write("\n".join(results))

    print(f"\n[Thành công] Đã xuất toàn bộ số liệu ra file bảng '{filename}' để nộp GitHub!")

if __name__ == "__main__":
    run_nqueens_benchmark()