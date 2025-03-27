import uuid


class VoteCollector:
    def __init__(self, pp, ame, candidate_list):
        """
        Initializes the Vote Collector with shared ElGamal parameters, Anamorphic ElGamal parameters,
        and the list of valid candidates.
        """
        self.pp = pp
        self.ame = ame
        self.candidate_list = candidate_list  # List of valid candidates
        # Generate vote collector's ElGamal private and public keys
        self.__sk, self.pk = pp.KeyGeneration()
        # Generate anamorphic keys for the vote collector using shared ElGamal public parameters
        self.__K, self.__T, self.pk = self.ame.AKeyGeneration(pp, self.pk)
        # Initialize list for encrypted votes
        self.__votes = []
        self.__user_data = {}

    def RegisterUser(self, user_pk, user_double_key):
        """Registers a user by storing their identity, public key, and double key."""
        user_id = str(uuid.uuid4())
        self.__user_data[user_id] = {
            "public_key": user_pk,
            "double_key": user_double_key
        }
        return user_id

    def GetDoubleKey(self, user_id):
        """Returns (K, T) only if the user is registered."""
        if user_id in self.__user_data:
            return self.__K, self.__T, self.pk  # Return the vote collector's double key
        else:
            raise ValueError("User not registered!")

    def DecryptVotes(self, ciphertext, user_id):
        """
        Decrypt the fake vote using the vote collector's secret key and the real vote using the double key.
        """
        fake_vote = self.pp.Decryption(self.__sk, ciphertext)
        real_vote = self.ame.ADecryption(self.pp, self.__K, self.__T, ciphertext)

        # Check if the real vote is valid (i.e., within the candidate list)
        if real_vote not in self.candidate_list:
            raise ValueError(f"Invalid real vote: {real_vote}. It is not in the candidate list.")
        else:
            self.__votes.append(self.pp.Encryption(self.pk,real_vote))

        return self.GenerateConfirmation(fake_vote, real_vote, user_id)

    def GenerateConfirmation(self, fake_vote, real_vote, user_id):
        """
        Create a single anamorphic ciphertext where the fake vote is the general value
        and the real vote is the hidden value, encrypted using the user's double key.
        """
        user_info = self.__user_data.get(user_id)
        if user_info:
            user_pk = user_info["public_key"]
            user_double_key = user_info["double_key"]
            confirmation_ciphertext = self.ame.AEncryption(self.pp, user_double_key[0], user_pk, fake_vote,
                                                           real_vote)
            return confirmation_ciphertext
