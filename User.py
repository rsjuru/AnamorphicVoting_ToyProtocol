
class User:
    def __init__(self, pp, ame, vc):
        """
        Initializes the user with ElGamal and Anamorphic ElGamal keys.
        Registers the user with the Vote Collector.
        """
        self.pp = pp
        self.ame = ame
        self.__sk, self.pk = pp.KeyGeneration()  # Private & Public keys
        self.__K, self.__T, self.pk = self.ame.AKeyGeneration(pp, self.pk)  # Anamorphic keys
        self.id = vc.RegisterUser(self.pk, [self.__K, self.__T])  # Get user ID from Vote Collector
        self.__vc_dk = vc.GetDoubleKey(self.id)  # Fetch Vote Collector's double key

        # Ensure the double key contains [K, T, pk] and nothing is missing
        if len(self.__vc_dk) != 3:
            raise ValueError("Invalid Vote Collector double key format!")

        self.__fv = None  # Fake vote
        self.__rv = None  # Real vote

    def EncryptVote(self, fake_vote, real_vote):
        """
        Encrypts the fake vote and real vote using anamorphic encryption.
        """
        self.__fv = fake_vote
        self.__rv = real_vote

        # Encrypt using Vote Collector's anamorphic key
        ciphertext = self.ame.AEncryption(self.pp, self.__vc_dk[0], self.__vc_dk[2], fake_vote, real_vote)

        return ciphertext

    def DecryptConfirmation(self, confirmation_ciphertext):
        """
        User decrypts the confirmation message from the vote collector.
        - Private key decrypts the fake vote.
        - Double key decrypts the real vote.
        - Votes are compared and result confirmed (faile/success)
        """
        fake_vote_confirmation = self.pp.Decryption(self.__sk, confirmation_ciphertext)
        real_vote_confirmation = self.ame.ADecryption(self.pp, self.__K, self.__T, confirmation_ciphertext)

        # Verify the decrypted votes match the original ones
        if fake_vote_confirmation == self.__fv and real_vote_confirmation == self.__rv:
            print("✅ Vote confirmed successfully!")
            return True
        else:
            print("❌ Vote confirmation failed! Possible tampering detected.")
            return False


