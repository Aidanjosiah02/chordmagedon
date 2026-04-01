from src.objects.Markov import Markov
from src.objects.Arrangement import Arrangement
from src.constants import ARRANGEMENT_LOG, ARRANGEMENT_PICKLE, DATASET, LOG_DIR, MARKOV_LOG_SUFFIX, MARKOV_PICKLE_SUFFIX, PROCESSED_DIR, Part
from src.utils.io_handler import log_arrangements, log_markov, parse_csv, write_pickle
from src.utils.parser import parse_arrangements

def run_dataset():
    print(f"\nLoading Dataset: {DATASET}")
    chord_strings = parse_csv(DATASET)
    
    print("Parsing arrangements...")
    arrangements = parse_arrangements(chord_strings)
    
    log_file = LOG_DIR / ARRANGEMENT_LOG
    pickle_file = PROCESSED_DIR / ARRANGEMENT_PICKLE
    
    print(f"Saving {len(arrangements)} arrangements...")
    log_arrangements(arrangements, log_file)
    write_pickle(arrangements, pickle_file)

    return arrangements

def run_markov_pipeline(arrangements: list[Arrangement], order: int) -> Markov:
    print(f"\nBuilding order-{order} Markov Chain")
    
    markov = Markov(order, Part.CHORDS)
    markov.build(arrangements)

    # Printing first entry as an example
    first_entry = next(iter(markov), None)
    if first_entry:
        context, transitions = first_entry
        print(f"Sample Entry: {context} -> {transitions}")

    # Generating filenames
    log_path = LOG_DIR / f"order{order}_{MARKOV_LOG_SUFFIX}"
    pickle_path = PROCESSED_DIR / f"order{order}_{MARKOV_PICKLE_SUFFIX}"

    print(f"Writing files to {PROCESSED_DIR}...")
    log_markov(markov.chain, log_path)
    write_pickle(markov, pickle_path)

    return markov

def main():
    arrangements: list[Arrangement] = run_dataset()
    
    # Run any number of Markov orders through the same pipeline
    markovs = [
        run_markov_pipeline(arrangements, order=1), 
        run_markov_pipeline(arrangements, order=2), 
        run_markov_pipeline(arrangements, order=3)
    ]

    # Fitness evaluation
    print("\nEvaluating arrangement fitness...")
    for arrangement in arrangements:
        arrangement.evaluate_fitness(markovs)
        # print(str(arrangement) + " = " + str(fitness))

    cliche = max(arrangements, key=lambda a: a.fitness)
    print(f"\nMost 'Cliche' Arrangement (Fitness: {cliche.fitness}):")
    print(cliche)

if __name__ == "__main__":
    main()
