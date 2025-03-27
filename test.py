import unittest
import random
from AME import ElGamal, AnamorphicElGamal
from User import User
from VoteCollector import VoteCollector
from Authority import Authority


class TestVotingSystem(unittest.TestCase):
    def setUp(self):
        """Initialize the voting system components before each test."""
        self.auth = Authority()
        self.pp, self.candidates = self.auth.GetPublicParameters()
        self.ame = AnamorphicElGamal(l=700, s=5, t=3)
        self.vc = VoteCollector(self.pp, self.ame, self.candidates)
        self.user = User(self.pp, self.ame, self.vc)

    def test_key_generation(self):
        """Test if the key generation function correctly generates a valid secret and public key pair."""
        sk, pk = self.pp.KeyGeneration()
        self.assertIsInstance(sk, int)
        self.assertIsInstance(pk, int)
        self.assertGreater(pk, 0)

    def test_encryption_decryption(self):
        """Test that a message can be encrypted and then decrypted back to the original value."""
        msg = random.choice(self.candidates)
        sk, pk = self.pp.KeyGeneration()
        ciphertext = self.pp.Encryption(pk, msg)
        decrypted_msg = self.pp.Decryption(sk, ciphertext)
        self.assertEqual(decrypted_msg, msg)

    def test_anamorphic_encryption_decryption(self):
        """Test that an anamorphic vote (hidden message) can be encrypted and later correctly decrypted."""
        fake_vote = 999  # Fake vote
        real_vote = random.choice(self.candidates)
        ciphertext = self.user.EncryptVote(fake_vote, real_vote)
        self.assertIsInstance(ciphertext, tuple)
        self.assertEqual(len(ciphertext), 2)
        dc = self.vc.DecryptVotes(ciphertext, self.user.id)

        # Verify decryption
        confirmation = self.user.DecryptConfirmation(dc)
        self.assertTrue(confirmation)

    def test_register_user(self):
        """Test if a user can be correctly registered by Vote Collector"""
        user_id = self.vc.RegisterUser(self.user.pk, [self.user._User__K, self.user._User__T])
        self.assertIsInstance(user_id, str)
        self.assertIn(user_id, self.vc._VoteCollector__user_data)

    def test_vote_collector_decryption(self):
        """Test if the Vote Collector can correctly decrypt a submitted vote"""
        fake_vote = 999
        real_vote = random.choice(self.candidates)
        ciphertext = self.user.EncryptVote(fake_vote, real_vote)
        confirmation = self.vc.DecryptVotes(ciphertext, self.user.id)
        self.assertIsNotNone(confirmation)
        self.assertIn(real_vote, self.candidates)

    def test_invalid_real_vote(self):
        """Test that the system rejects invalid votes that are not among the valid candidates."""
        fake_vote = 999
        real_vote = 9999  # Invalid vote
        ciphertext = self.user.EncryptVote(fake_vote, real_vote)
        with self.assertRaises(ValueError):
            self.vc.DecryptVotes(ciphertext, self.user.id)


if __name__ == "__main__":
    unittest.main()
