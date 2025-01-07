from multiprocessing import Pool
import itertools

def check_password(attempt_tuple):
    target_password = "abc1"
    attempt = ''.join(attempt_tuple)
    if attempt == target_password:
        return attempt
    return None

if __name__ == "__main__":
    charset = "abc123"
    repeat = 4
    target_password = "abc1"

    # Générer toutes les combinaisons possibles
    combinations = itertools.product(charset, repeat=repeat)

    # Créer un pool de travailleurs pour accélérer le traitement
    with Pool() as pool:
        for result in pool.imap_unordered(check_password, combinations):
            if result:
                print(f"Password found: {result}")
                pool.terminate()  # Arrêter dès que le mot de passe est trouvé
                break
