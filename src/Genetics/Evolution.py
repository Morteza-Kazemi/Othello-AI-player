import math
from random import *
from src.Genetics.Agent_vs_agent import AgentVsAgent
import src.Genetics.Gene as GeneFile

# Constant values
MIN_WEIGHT = 1
MAX_WEIGHT = 200
NUM_OF_FEATURES = 9  # TODO: change
TOTAL_POPULATION = 25  # TODO: may need to change
BEST_GENE_SIZE = 6
WORST_GENE_SIZE = 2
BEST_GENE_CROSOV_SIZE = 9
WORST_GENE_CROSOV_SIZE = 1
BEST_WORST_CROSOV_SIZE = 7
LEAGUE_SIZE = 5


class Evolution:

    def __init__(self):
        self.generation_number = 1
        self.generation_limit = 3  # TODO: may need to change
        self.gene_list = []
        self.mutation_probability = 0.2  # is divided by generation number when mutating
        self.log_history = ""

    def init_generation(self):
        """ Generate initial generation (first population)
            first generation is randomly selected """

        for i in range(TOTAL_POPULATION):
            random_list = [randint(MIN_WEIGHT, MAX_WEIGHT) for i in range(NUM_OF_FEATURES - 1)]
            random_list.append(randint(MIN_WEIGHT, MIN_WEIGHT + 10))  # last feature is not much important
            self.gene_list.append(GeneFile.Gene(random_list))

    def next_generation(self):
        """ Generate next generation
            some genes are directly moved to next generation
            other genes are created using crossover (some are mutated in crossover function)
            generation size is not changed
            """

        self.sort_genes()  # sort list of gens by fitness value

        # grouping current population into two groups of best and worst
        best_list = self.gene_list[:BEST_GENE_SIZE]
        worst_list = self.gene_list[BEST_GENE_SIZE: TOTAL_POPULATION]

        # set the next generation
        new_generation = best_list
        new_generation.extend(self.random_genes(WORST_GENE_SIZE, worst_list))
        new_generation.extend(self.cross_over(best_list, BEST_GENE_CROSOV_SIZE, False))
        new_generation.extend(self.cross_over(worst_list, WORST_GENE_CROSOV_SIZE, False))
        new_generation.extend(self.cross_over(self.gene_list, BEST_WORST_CROSOV_SIZE, True))

        # change the current population to next generation
        self.gene_list = new_generation

    def cross_over(self, parents_list, children_size, is_separated):
        """ creates new genes using a weighted average of parents features
            mutates the new genes with a probability decreasing in each next generation"""

        children_list = []
        for i in range(children_size):
            parents = []
            # check if the list of desired parents are separated
            if is_separated:  # a parent from best and a parent from worse list
                best_list = self.gene_list[:BEST_GENE_SIZE]
                worst_list = self.gene_list[BEST_GENE_SIZE: TOTAL_POPULATION]
                parents.extend(self.random_genes(1, best_list))
                parents.extend(self.random_genes(1, worst_list))
            else:  # both parents from given parent list
                parents = self.random_genes(2, parents_list)  # choose parents for the new gene

            new_weight_list = []  # feature values for the gene (weights)
            alpha = random()  # parameter used for finding weighted average of parents features

            # set each feature of the new gene to the weighted average of parents features
            for j in range(NUM_OF_FEATURES):
                new_weight_list.append(math.floor((alpha * parents[0].weight_list[j] +
                                                   (1 - alpha) * parents[1].weight_list[j])))
            # mutation with a probability
            new_weight_list = self.mutate(new_weight_list)

            # add the gene to children_list
            child = GeneFile.Gene(new_weight_list)

            # log parents and crossover result
            # self.handle_logs(
            #     self.list_to_str(parents[0].weight_list) + self.list_to_str(parents[1].weight_list)
            #     + "{0:.2f}".format(alpha) + self.list_to_str(child.weight_list) + '\n')

            children_list.append(child)

        return children_list

    def mutate(self, weight_list):
        """ mutates the genes by subtracting or adding a random value to one of the features of the gene(the feature
        is selected randomly) """

        probability = self.mutation_probability / self.generation_number  # reduced in each generation for better
        # exploitation

        rand = random()
        if rand < probability:

            # randomly choose a feature and a bias for mutation
            mutating_index = randrange(0, NUM_OF_FEATURES)
            bias = randrange(-50, 50)

            weight_list[mutating_index] += bias

            # check if the feature exceeds the lower or upper bound of weight value
            if weight_list[mutating_index] > MAX_WEIGHT:
                weight_list[mutating_index] = MAX_WEIGHT
            elif weight_list[mutating_index] < MIN_WEIGHT:
                weight_list[mutating_index] = MIN_WEIGHT

        return weight_list

    def play_generation(self, league_start_indx, league_end_indx):
        """ simulates game for each two different genes in the league
            updates gene properties: total_games and total_wins
            """

        game_number = 0  # counts the number of games played in each generation

        league_list = self.gene_list[league_start_indx:league_end_indx]

        for i in range(LEAGUE_SIZE):
            gene1 = league_list[i]
            for j in range(i + 1, LEAGUE_SIZE):
                gene2 = league_list[j]

                self.handle_logs("*************************" + '\n' +
                                 "genes fight: " + str(game_number) + " " + self.list_to_str(gene1.weight_list)
                                 + " vs " + self.list_to_str(gene2.weight_list) + '\n')

                game_number += 1
                gene1.increment_total_game()
                gene2.increment_total_game()

                # simulate ai_vs_ai game and find the winner
                winner = self.play_ai_vs_ai(gene1, gene2)

                if winner is None:  # game was tie
                    gene1.increment_for_tie()
                    gene2.increment_for_tie()
                    self.handle_logs("tie" + '\n')
                else:
                    winner.increment_for_winning()
                    self.handle_logs("winner is: " + self.list_to_str(winner.weight_list) + '\n')

        # update genes in gene_list
        self.gene_list[league_start_indx:league_end_indx] = league_list

    @staticmethod
    def play_ai_vs_ai(gene1: GeneFile.Gene, gene2: GeneFile.Gene):
        """ game is simulated between the input genes and the winner gene is returned"""

        winner_gene = AgentVsAgent(gene1, gene2).get_winner()
        return winner_gene

    def run(self):
        """ runs the game for all desired generations
            and prints the best gene in the final generation(the gene we are looking for)
            logs each generation genes to a file
            """
        # select the initial population
        self.init_generation()

        while self.generation_number <= self.generation_limit:
            self.handle_logs("*********************************************" + '\n' +
                             "generation number " + str(self.generation_number) + '\n')
            for gene in self.gene_list:
                self.handle_logs(self.list_to_str(gene.weight_list) + '\n')

            # run the game for all pairs of genes in each league
            for i in range(LEAGUE_SIZE):
                self.play_generation(i*LEAGUE_SIZE, (i+1)*LEAGUE_SIZE)

            self.log_generation_to_file()

            if self.generation_number == self.generation_limit:
                break
            self.generation_number += 1
            self.next_generation()

        # print the best gene in the final generation
        self.sort_genes()
        self.handle_logs(".................................\n" + "OPTIMUM WEIGHT LIST \n" +
                         self.list_to_str(self.gene_list[0].weight_list) + '\n')

    def sort_genes(self):
        """ sorts self.gene_list using genes fitness values"""
        for gene in self.gene_list:
            gene.fitness_calc()
        self.gene_list = sorted(self.gene_list, key=self.cmp_fitness, reverse=True)

    def log_generation_to_file(self):
        f = open("log" + str(self.generation_number) + ".txt", "w")
        f.write(self.log_history)
        f.close()
        self.log_history = " "

    def handle_logs(self, message):
        self.log_history += message
        print(message, end="")

    @staticmethod
    def random_genes(size, gene_list):
        """ randomly selects a number of 'size' genes from the given gene_list"""
        return sample(gene_list, size)

    @staticmethod
    def cmp_fitness(gene):
        return gene.fitness

    @staticmethod
    def list_to_str(list_):
        """ casts input list to a string """
        return "[" + " ".join(str(x) for x in list_) + "]"


if __name__ == '__main__':
    Evolution().run()
