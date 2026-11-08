import random
import statistics

cap = [20, 15, 35, 40, 15, 15, 10]
n = [2, 2, 1, 1, 1, 1, 1]
dem = [80, 90, 65, 70]
nunite, ninterv = len(cap), len(dem)
total = sum(cap)

def patterns_valides(k):
    res = []
    for i in range(ninterv - k + 1):
        bits = [0] * ninterv
        for j in range(i, i + k):
            bits[j] = 1
        res.append(tuple(bits))
    return res

p = [patterns_valides(k) for k in n]
def individu_aleatoire():
    return [random.choice(p[u]) for u in range(nunite)]

def reserves(ch):
    res = []
    for t in range(ninterv):
        perdue = sum(cap[u] for u in range(nunite) if ch[u][t])
        res.append(total - perdue - dem[t])
    return res

def performance(ch):
    return max(0, min(reserves(ch)))

def selection_loterie(pop, perfs):
    poids = [p + 1e-6 for p in perfs]
    return random.choices(pop, weights=poids, k=1)[0]

def croisement(p1, p2, pc):
    if random.random() > pc:
        return p1[:], p2[:]
    pt = random.randint(1, nunite - 1)
    return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]

def mutation_inversion(ch, pm):
    enfant = ch[:]
    for u in range(nunite):
        if random.random() < pm:
            enfant[u] = tuple(reversed(enfant[u]))
    return enfant

def mutation_remplacement(ch, pm):
    enfant = ch[:]
    for u in range(nunite):
        if random.random() < pm:
            enfant[u] = random.choice(p[u])
    return enfant

def algo_genetique(taille_pop=40, generations=60, pc=0.8, pm=0.15,mutation=mutation_inversion, elitisme=True, graine=None):
    if graine is not None:
        random.seed(graine)
    pop = [individu_aleatoire() for _ in range(taille_pop)]
    historique = []
    meilleur = max(pop, key=performance)
    for g in range(generations):
        perfs = [performance(c) for c in pop]
        b = pop[perfs.index(max(perfs))]
        if performance(b) > performance(meilleur):
            meilleur = b[:]
        historique.append(max(perfs))
        nouvelle = [meilleur[:]] if elitisme else []
        while len(nouvelle) < taille_pop:
            p1 = selection_loterie(pop, perfs)
            p2 = selection_loterie(pop, perfs)
            e1, e2 = croisement(p1, p2, pc)
            nouvelle += [mutation(e1, pm), mutation(e2, pm)]
        pop = nouvelle[:taille_pop]
    return meilleur, historique

def afficher(ch):
    print("Chromosome :", " ".join("".join(map(str, g)) for g in ch))
    for u, g in enumerate(ch, 1):
        ints = [str(t + 1) for t in range(ninterv) if g[t]]
        print(f"  Unité {u} ({cap[u-1]} MW) : maintenance aux intervalles {', '.join(ints)}")
    print("Réserves par intervalle :", reserves(ch))
    print("Performance (réserve min) :", performance(ch))

if __name__ == "__main__":
    ex = [(0,1,1,0), (0,0,1,1), (0,0,0,1), (1,0,0,0), (0,1,0,0), (0,0,1,0), (1,0,0,0)]
    afficher(ex)
    sol, hist = algo_genetique(mutation=mutation_inversion, graine=1)
    afficher(sol)
    print("Meilleure perf par génération :", hist[::10], "...", hist[-1])
    print("Comparaison des mutations")
    for nom, mut in [("inversion", mutation_inversion), ("remplacement", mutation_remplacement)]:
        res = [performance(algo_genetique(mutation=mut, graine=s)[0]) for s in range(30)]
        print(f"  {nom:13s} moyenne={statistics.mean(res):.1f}  max={max(res)}  "f"optimum atteint {res.count(max(res))}/30")