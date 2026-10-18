import math
import random
import copy

random.seed(1)
INF = float("inf")
d = {}
d[(1, 2)], d[(1, 3)], d[(1, 8)] = 14, 15, 17
d[(2, 3)], d[(2, 4)], d[(2, 5)], d[(2, 8)] = 13, 14, 20, 21   
d[(3, 4)], d[(3, 5)], d[(3, 6)], d[(3, 7)], d[(3, 8)] = 11, 21, 17, 9, 9
d[(4, 5)], d[(4, 6)], d[(4, 7)], d[(4, 8)] = 11, 10, 8, 20
d[(5, 6)], d[(5, 7)] = 15, 18                            
d[(6, 7)] = 9                                           
d[(7, 8)] = 13
N = 8

def taboue(initial, nb_iter=30, taille_tabou=4):
    courant = list(initial)
    meilleur, f_meilleur = list(courant), longueur(courant)
    tabou = []
    print("\n--- RECHERCHE TABOUE ---")
    print(f"Solution initiale : {affiche(courant)}   L = {longueur(courant)}")
    for it in range(1, nb_iter + 1):
        candidats = []
        for mvt, nv in voisins_2opt(courant):
            f = longueur(nv)
            if f == INF:
                continue                     
            if mvt in tabou and f >= f_meilleur:
                continue                     
            candidats.append((f, mvt, nv))
        if not candidats:
            break
        f, mvt, nv = min(candidats, key=lambda c: c[0])
        courant = nv
        tabou.append(mvt)
        if len(tabou) > taille_tabou:
            tabou.pop(0)
        if f < f_meilleur:
            meilleur, f_meilleur = list(nv), f
        print(f"it {it:2d} : mvt 2-opt{mvt}  {affiche(courant)}  L = {f}  (meilleur = {f_meilleur})")
    return meilleur, f_meilleur

def dist(a, b):
    return d.get((min(a, b), max(a, b)), INF)

def longueur(tour):
    return sum(dist(tour[i], tour[(i + 1) % N]) for i in range(N))

def affiche(tour):
    return "-".join(map(str, tour)) + "-" + str(tour[0])

def voisins_2opt(tour):
    for i in range(1, N - 1):
        for j in range(i + 1, N):
            nv = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
            yield (i, j), nv

def recuit(initial, T0=20.0, alpha=0.8, T_min=0.5, iter_palier=5):
    courant = list(initial)
    f_courant = longueur(courant)
    meilleur, f_meilleur = list(courant), f_courant
    T = T0
    print(f"\n--- RECUIT SIMULE (T0={T0}, alpha={alpha}, {iter_palier} it/palier) ---")
    print(f"Solution initiale : {affiche(courant)}   L = {f_courant}")

    while T > T_min:
        for _ in range(iter_palier):
            _, nv = random.choice(list(voisins_2opt(courant)))
            f_nv = longueur(nv)
            if f_nv == INF:
                continue
            delta = f_nv - f_courant
            if delta <= 0 or random.random() < math.exp(-delta / T):
                courant, f_courant = nv, f_nv
                if f_courant < f_meilleur:
                    meilleur, f_meilleur = list(courant), f_courant
        print(f"T = {T:6.2f} : courant L = {f_courant:3}   meilleur L = {f_meilleur}")
        T *= alpha
    return meilleur, f_meilleur

def essai_variation_T():
    print("\n=== Variation empirique de la température initiale ===")
    init = [1, 2, 3, 4, 5, 6, 7, 8]
    resultats = []
    for T0 in (5, 10, 20, 50, 100):
        moyenne = []
        for graine in range(30):
            random.seed(graine)
            c, f = _recuit_silencieux(init, T0)
            moyenne.append(f)
        resultats.append((T0, min(moyenne), sum(moyenne) / len(moyenne)))
        print(f"T0 = {T0:3} : meilleur = {min(moyenne)}   moyenne sur 30 essais = {sum(moyenne)/len(moyenne):.1f}")
    return resultats

def optimum_exact():
    import itertools
    best, fb = None, INF
    for p in itertools.permutations(range(2, N + 1)):
        t = [1] + list(p)
        f = longueur(t)
        if f < fb:
            best, fb = t, f
    return best, fb

def _recuit_silencieux(initial, T0, alpha=0.8, T_min=0.5, iter_palier=5):
    courant = list(initial); f_c = longueur(courant)
    best, f_b = list(courant), f_c
    T = T0
    while T > T_min:
        for _ in range(iter_palier):
            _, nv = random.choice(list(voisins_2opt(courant)))
            f = longueur(nv)
            if f == INF:
                continue
            delta = f - f_c
            if delta <= 0 or random.random() < math.exp(-delta / T):
                courant, f_c = nv, f
                if f_c < f_b:
                    best, f_b = list(courant), f_c
        T *= alpha
    return best, f_b

if __name__ == "__main__":
    depart = [1, 2, 3, 4, 5, 6, 7, 8]
    bt, ft = taboue(depart)
    print(f"\n>>> Taboue : {affiche(bt)}  L = {ft}")
    random.seed(1)
    br, fr = recuit(depart)
    print(f"\n>>> Recuit simulé : {affiche(br)}  L = {fr}")
    essai_variation_T()
    bo, fo = optimum_exact()
    print(f"\nVérification (énumération complète) : {affiche(bo)}  L = {fo}")
