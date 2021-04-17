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

    def tournament(self, functions, fitnesses):
        idxs = random.sample(list(range(len(functions))), self.tournament_size)
        tournament = [(fitnesses[idx], idx) for idx in idxs]
        winner = sorted(tournament, key=lambda x: x[0])[-1]
        return functions[winner[1]]

    def choose_winners(self, functions, fitnesses):
        winners = []
        hall_of_fame = self.runs[-1].hall_of_fame
        for _ in range(self.generation_size - len(hall_of_fame)):
            winner = self.tournament(functions, fitnesses)
            donor = self.tournament(functions, fitnesses)
            winners.append((winner, donor))
        for champion in hall_of_fame:
            winner = self.tournament(functions, fitnesses)
            winners.append((winner, champion))
        return winners

    def initialise_run(self):
        recorder = RunRecord(self.run_idx)
        self.runs.append(recorder)
        self.run_idx += 1
        return recorder

    def breed(self):
        recorder = self.initialise_run()
        initial_functions = list(self.maker.generate_functions(self.starting_functions))
        initial_fitnesses = self.fitness(initial_functions)
        recorder.record(initial_functions, initial_fitnesses, None)
        winners = self.choose_winners(initial_functions, initial_fitnesses)
        for gen in range(self.n_generations):
            functions = []
            all_stats = []
            for name_idx, (winner, donor) in enumerate(winners):
                baby, stats = self.maker.make_baby(winner, donor, name_idx=name_idx)
                functions.append(baby)
                all_stats.append(stats)
            functions = [func for func in functions if func is not None]
            fitnesses = self.fitness(functions)
            winners = self.choose_winners(functions, fitnesses)
            recorder.record(functions, fitnesses, all_stats)
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
        self.summaries.append(self.summarise_stats(stats, fitnesses))
        self.report(fitnesses)
        self.generation += 1

    def report(self, fitnesses):
        score = sum(fitnesses) / len(fitnesses)
        print(f"Average fitness for generation {self.generation} is {round(score, 2)}")

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
            for stat in ["time", "parent_1_size", "parent_2_size", "failures"]:
                ns = [s[stat] for s in stats]
                out[stat] = self.summarise(ns)
        out["fitness"] = self.summarise(fitnesses)
        return out
