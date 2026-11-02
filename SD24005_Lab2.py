import random
import streamlit as st

POP_SIZE = 300        
IND_LENGTH = 80       
TARGET_ONES = 50      
N_GEN = 50            


CX_PROB = 0.9
MUT_PROB = 0.02       
TOURN_SIZE = 3



def fitness(ind):
    # maximum value = 80 when the number of ones = 50
    return IND_LENGTH - abs(sum(ind) - TARGET_ONES)


def create_individual():
    return [random.randint(0, 1) for _ in range(IND_LENGTH)]


def create_population():
    return [create_individual() for _ in range(POP_SIZE)]


def selection(pop):
    group = random.sample(pop, TOURN_SIZE)
    return max(group, key=fitness)[:]


def crossover(p1, p2):
    if random.random() < CX_PROB:
        point = random.randint(1, IND_LENGTH - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        return c1, c2
    return p1[:], p2[:]


def mutation(ind):
    for i in range(len(ind)):
        if random.random() < MUT_PROB:
            ind[i] = 1 - ind[i]
    return ind


def run_ga():
    pop = create_population()
    best_history = []
    avg_history = []
    best_ever = max(pop, key=fitness)[:]

    for gen in range(N_GEN):
        fits = [fitness(ind) for ind in pop]
        best_history.append(max(fits))
        avg_history.append(sum(fits) / len(fits))

        gen_best = max(pop, key=fitness)
        if fitness(gen_best) > fitness(best_ever):
            best_ever = gen_best[:]

        
        new_pop = [best_ever[:]]
        while len(new_pop) < POP_SIZE:
            p1 = selection(pop)
            p2 = selection(pop)
            c1, c2 = crossover(p1, p2)
            new_pop.append(mutation(c1))
            if len(new_pop) < POP_SIZE:
                new_pop.append(mutation(c2))
        pop = new_pop

    return best_ever, best_history, avg_history


st.title("Genetic Algorithm - Bit Pattern")

st.subheader("Parameters")
st.write(f"- Population size: {POP_SIZE}")
st.write(f"- Individual length: {IND_LENGTH}")
st.write(f"- Number of ones for max fitness: {TARGET_ONES} (fitness = {IND_LENGTH})")
st.write(f"- Number of generations: {N_GEN}")
st.write("- Fitness function: `80 - abs(number of ones - 50)`")

if st.button("Run Genetic Algorithm"):
    best, best_hist, avg_hist = run_ga()

    st.subheader("Result")
    st.write("Best bit pattern:")
    st.code("".join(str(b) for b in best))
    st.write("Number of ones:", sum(best))
    st.write("Fitness value:", fitness(best))

    if fitness(best) == IND_LENGTH:
        st.success("Maximum fitness reached!")
    else:
        st.warning("Maximum fitness not reached, try running again.")

    st.subheader("Fitness over generations")
    chart_data = {"Best fitness": best_hist, "Average fitness": avg_hist}
    st.line_chart(chart_data)

    st.subheader("Table of generations")
    table = {
        "Generation": list(range(1, N_GEN + 1)),
        "Best fitness": best_hist,
        "Average fitness": [round(a, 2) for a in avg_hist],
    }
    st.dataframe(table)