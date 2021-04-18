from drawing.regulate import regulate
import random


class Breeder:
    def __init__(
        self,
        maker,
        fitness_function,
        starting_functions=500,
        generation_size=100,
        n_generations=5,
        tournament_size=5,
        stopping_fitness=None,
    ):
        self.maker = maker
        self.fitness_function = fitness_function
        self.starting_functions = starting_functions
        self.generation_size = generation_size
        self.tournament_size = tournament_size
        self.n_generations = n_generations
        self.stopping_fitness = stopping_fitness
        self.runs = []
        self.run_idx = 0

    def fitness(self, functions):
        fitnesses = []
        for func in functions:
            try:
                outputs = [regulate(func(i)) for i in range(10)]
            except (KeyError, ValueError, TypeError, ZeroDivisionError):
                outputs = []
            fitnesses.append(self.fitness_function(outputs))
        return fitnesses

    def adjust_for_sizes(self, fitnesses, idxs, sizes):
        adjust = max(fitnesses)
        sizes = [(float(i) / sum(sizes)) * adjust for i in sizes]
        tournament = [(fitnesses[idx] - sizes[idx], idx) for idx in idxs]
        return tournament

    def tournament(self, functions, fitnesses, sizes):
        idxs = random.sample(list(range(len(functions))), self.tournament_size)
        if sizes is not None:
            tournament = self.adjust_for_sizes(fitnesses, idxs, sizes)
        else:
            tournament = [(fitnesses[idx], idx) for idx in idxs]
        winner = sorted(tournament, key=lambda x: x[0])[-1]
        return functions[winner[1]]

    def choose_winners(self, functions, fitnesses, sizes=None):
        winners = []
        for _ in range(self.generation_size):
            winner = self.tournament(functions, fitnesses, sizes)
            donor = self.tournament(functions, fitnesses, sizes)
            winners.append((winner, donor))
        return winners

    def initialise_run(self):
        recorder = RunRecord(self.run_idx)
        self.runs.append(recorder)
        self.run_idx += 1
        return recorder

    def breed(self):
        recorder = self.initialise_run()
        print(f"Generating {self.starting_functions} random functions")
        initial_functions = list(self.maker.generate_functions(self.starting_functions))
        initial_fitnesses = self.fitness(initial_functions)
        recorder.record(initial_functions, initial_fitnesses, None)
        winners = self.choose_winners(initial_functions, initial_fitnesses)
        for gen in range(self.n_generations):
            functions = []
            all_stats = []
            for name_idx, (winner, donor) in enumerate(winners):
                baby, stats = self.maker.make_baby(
                    winner, donor, name_idx="_".join([str(gen), str(name_idx)])
                )
                functions.append(baby)
                all_stats.append(stats)
            functions = [func for func in functions if func is not None]
            fitnesses = self.fitness(functions)
            sizes = [s["size"] for s in all_stats]
            winners = self.choose_winners(functions, fitnesses, sizes=sizes)
            recorder.record(functions, fitnesses, all_stats)
            score = sum(fitnesses) / len(fitnesses)
            if self.stopping_fitness and score > self.stopping_fitness:
                break

    def best_function(self, run=-1, generation=-1):
        func = self.runs[run].hall_of_fame[generation]
        return self.maker.source_for_function(func)

    def hall_of_fame(self, run=-1):
        hall_of_fame = []
        for func in self.runs[run].hall_of_fame:
            hall_of_fame.append(self.maker.function_converter.source_for_function(func))
        return hall_of_fame


class RunRecord:
    def __init__(self, run_idx):
        print(f"Starting run {run_idx}")
        self.run_idx = run_idx
        self.hall_of_fame = []
        self.stats = []
        self.fitnesses = []
        self.summaries = []
        self.generation = 0

    def record(self, functions, fitnesses, stats):
        best_function = self.best_function(functions, fitnesses)
        self.hall_of_fame.append(best_function)
        self.stats.append(stats)
        self.fitnesses.append(fitnesses)
        summary = self.summarise_stats(stats, fitnesses)
        self.summaries.append(summary)
        self.report(summary)
        self.generation += 1

    def report(self, summary):
        fitness = round(summary["fitness"]["avg"], 2)
        size = int(summary.get("size", {}).get("avg", 0))
        print(
            f"Average fitness for generation {self.generation} is {fitness} with an average size of {size} nodes."
        )

    def best_function(self, functions, fitnesses):
        return functions[fitnesses.index(max(fitnesses))]

    def summarise(self, ns):
        out = {}
        idx = int(len(ns) * 0.95)
        avg = sum(ns) / len(ns)
        ntile = sorted(ns)[idx]
        ntile_ = sorted(ns)[-idx]
        out[f"avg"] = avg
        out[f"95th"] = ntile
        out[f"5th"] = ntile_
        return out

    def summarise_stats(self, stats, fitnesses):
        out = {}
        if stats is not None:
            for stat in ["time", "size", "failures"]:
                ns = [s[stat] for s in stats]
                out[stat] = self.summarise(ns)
        out["fitness"] = self.summarise(fitnesses)
        return out
