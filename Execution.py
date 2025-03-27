from Authority import Authority
from User import User
from VoteCollector import VoteCollector
import AME
import time
import random


def execute():
    start_time = time.time()

    # 1️⃣ Initialize Authority and AME
    print("Initializing Authority and AME...")
    authority = Authority()
    ame = AME.AnamorphicElGamal(700, 10, 10)

    # Get public parameters and candidates
    elgamal, candidate_list = authority.GetPublicParameters()
    print(random.choice(candidate_list))

    # 2️⃣ Initialize VoteCollector and User
    print("Initializing VoteCollector and User...")
    vote_collector = VoteCollector(elgamal, ame, candidate_list=candidate_list)

    keygen_start = time.time()
    user = User(elgamal, ame, vote_collector)  # Key generation happens here
    keygen_end = time.time()

    print(f"✅ Key Generation Time: {(keygen_end - keygen_start)*10**3:.6f} seconds")

    # 3️⃣ Encrypt the vote
    print("Encrypting vote...")
    encrypt_start = time.time()
    encrypted_votes = user.EncryptVote(43, random.choice(candidate_list))
    encrypt_end = time.time()

    print(f"✅ Encryption Time: {(encrypt_end - encrypt_start)*10**3:.6f} ms")

    # 4️⃣ VoteCollector decrypts the votes
    print("VoteCollector processing encrypted votes...")
    decrypt_start = time.time()
    confirmation_ciphertext = vote_collector.DecryptVotes(encrypted_votes, user.id)
    decrypt_end = time.time()

    print(f"✅ VoteCollector Decryption Time: {(decrypt_end - decrypt_start)*10**3:.6f} ms")

    # 5️⃣ User decrypts the confirmation
    print("User decrypting confirmation...")
    confirm_start = time.time()
    user.DecryptConfirmation(confirmation_ciphertext)
    confirm_end = time.time()

    print(f"✅ Confirmation Decryption Time: {(confirm_end - confirm_start)*10**3:.6f} ms")

    total_time = time.time() - start_time
    print(f"\n⏱️ Total Execution Time: {total_time*10**3:.6f} ms")


# Execute the process
execute()
