import random
import itertools

random.seed(42)
cout = [[5, 3, 4],
        [6, 7, 2]]
offre = [8, 9]
demande = [4, 5, 8]
nb_mag = len(demande)

def solution_initiale():
    x1 = [0] * nb_mag
    reste = offre[0]
    ordre = list(range(nb_mag))
    random.shuffle(ordre)
    for j in ordre:
        q = min(reste, demande[j])
        x1[j] = q
        reste -= q
    return x1

def complete(x1):
    return [list(x1), [demande[j] - x1[j] for j in range(nb_mag)]]

def cout_total(x1):
    x = complete(x1)
    return sum(cout[i][j] * x[i][j] for i in range(2) for j in range(nb_mag))

def faisable(x1):
    return (sum(x1) == offre[0]
            and all(0 <= x1[j] <= demande[j] for j in range(nb_mag)))

def voisinage(x1):
    for j in range(nb_mag):
        for k in range(nb_mag):
            if j != k:
                y = list(x1)
                y[j] -= 1
                y[k] += 1
                if faisable(y):
                    yield (j, k), y

def recherche_taboue(nb_iter=12, taille_tabou=3):
    courant = [0, 0, 8] 
    meilleur, f_meilleur = list(courant), cout_total(courant)
    tabou = []        
    print(f"Solution initiale : D1 = {courant}  coût = {cout_total(courant)}")
    for it in range(1, nb_iter + 1):
        candidats = []
        for mvt, y in voisinage(courant):
            f = cout_total(y)
            inverse = (mvt[1], mvt[0])
            if inverse in tabou and f >= f_meilleur:
                continue
            candidats.append((f, mvt, y))
        if not candidats:
            break
        f, mvt, y = min(candidats, key=lambda c: c[0])
        courant = y
        tabou.append(mvt)
        if len(tabou) > taille_tabou:
            tabou.pop(0)
        if f < f_meilleur:
            meilleur, f_meilleur = list(y), f
        print(f"it {it:2d} : mvt {mvt} -> D1 = {courant}  coût = {f}  (meilleur = {f_meilleur})")
    return meilleur, f_meilleur

def enumeration_exacte():
    best, fbest = None, float("inf")
    for x1 in itertools.product(*[range(d + 1) for d in demande]):
        if faisable(x1) and cout_total(x1) < fbest:
            best, fbest = list(x1), cout_total(x1)
    return best, fbest

if __name__ == "__main__":
    best, f = recherche_taboue()
    x = complete(best)
    print("\n=== Résultat recherche taboue ===")
    print("        M1  M2  M3")
    print("D1     ", x[0])
    print("D2     ", x[1])
    print("Coût total minimal trouvé :", f)
    b2, f2 = enumeration_exacte()
    print("\nVérification par énumération exacte :", complete(b2), "coût =", f2)
