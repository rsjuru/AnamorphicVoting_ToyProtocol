from AME import ElGamal


class Authority:
    def __init__(self):
        """
        Initializes the Authority with global ElGamal parameters and Anamorphic ElGamal parameters.
        """
        p, g = int(1000000000007), 5  # Oakley group (RFC 2409)
        q = p - 1
        elgamal = ElGamal(p, q, g)
        self.elgamal = elgamal

        self.sk, self.pk = self.elgamal.KeyGeneration()
        self.candidate_list = list(range(1, 701))

    def GetPublicParameters(self):
        """
        Return the global public parameters (p, q, g) for ElGamal and Anamorphic ElGamal.
        """
        return self.elgamal, self.candidate_list
