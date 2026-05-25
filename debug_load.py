from datasets import load_dataset
try:
    ds = load_dataset("electricsheepafrica/nigerian_energy_and_utilities_demand_forecasting")
    print("Success!")
    print(ds)
except Exception as e:
    import traceback
    traceback.print_exc()
