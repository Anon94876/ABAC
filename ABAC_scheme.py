from charm.toolbox.pairinggroup import PairingGroup, G1, G2, GT, ZR, pair
from charm.toolbox.hash_module import Hash
import hashlib
import time

# Initialize the pairing group (this automatically selects a specific pairing scheme)
group = PairingGroup('SS512')  # Use 'SS512' or 'MNT160', 'MNT224' etc., depending on the group you want

# Define hash functions
def H1(input_string):
    return group.hash(input_string, G1)

def H2(input_string):
    return group.hash(input_string, ZR)  # Corrected: Hash to the scalar field Zr

def H3(input_string):
    return group.hash(input_string, G1)

# Key Generation for STTP (Secret Key Generator)
def PartialKeyGen(ID, Attr, s):
    Q = H1(ID + Attr)
    start = time.time()
    D = Q ** s  # D = Q^s
    end = time.time()
    end = time.time()
    print(f"[Benchmark] Exponentiation time: {(end - start)*1000:.4f} ms")
    return D

# Key Generation for User
def KeyGen(s, D):
    x = group.random()  
    P = group.init(G1, group.random())  # Public key component (P = g^x)
    pk = P
    sk = (x, D)  # Private key = (x, D)
    print(pk,sk)
    return pk, sk

# Sign a Message
def Sign(M, Attr, D, x):
    start = time.time()
    h = H2(M + Attr)
    end = time.time()
    print(f"[Benchmark] H2 time: {(end - start)*1000:.4f} ms")
    start = time.time()
    R = H3(M + Attr)  # Random group element for the signature
    end = time.time()
    print(f"[Benchmark] H3 time: {(end - start)*1000:.4f} ms")
    start = time.time()
    sigma = (D * R) ** x  # Signature σ = (D · R)^x
    end = time.time()
    print(f"[Benchmark] Multiplication time: {(end - start)*1000:.4f} ms")
    return sigma, R

# Verify the Signature
def ServerVerify(M, Attr, sigma, P, P0, ID):
    start = time.time()
    Q = H1(ID + Attr) # Q = H1(ID || Attr)
    end = time.time()
    print(f"[Benchmark] H1 time: {(end - start)*1000:.4f} ms") 
    R = H3(M + Attr)  # R = H3(M || Attr)
    
    # Compute the pairings
    start = time.time()
    V1 = pair(sigma, group.init(G1, 1))  # e(σ, g)
    V2 = pair(Q, P0) * pair(R, P)  # e(Q, P0) * e(R, P)
    end = time.time()
    print(f"[Benchmark] Bilinear pairing time: {(end - start)*1000:.4f} ms") 
    return V1 == V2

# Main function to demonstrate the signing and verification process
def main():
    # Step 1: Setup (STTP's key generation)
    s = group.random()  # Master secret key (random) — corrected to use group.random()
    P0 = group.init(G1, group.random()) ** s  # Public key (P0 = g^s)
    
    # Step 2: Partial Key Generation
    ID = "user1"  # Identity of the user
    Attr = "admin"  # Attributes associated with the user
    D = PartialKeyGen(ID, Attr, s)  # D = Q^s (partial key)

    # Step 3: User's Key Generation
    pk, sk = KeyGen(s, D)  # User's public and private keys

    # Step 4: Signing a message
    M = "This is a secret message"  # Message to be signed
    sigma, R = Sign(M, Attr, D, sk[0])  # Create the signature

    # Step 5: Verification by the server
    valid = ServerVerify(M, Attr, sigma, pk, P0, ID)
    if valid:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")

if __name__ == '__main__':
    main()

