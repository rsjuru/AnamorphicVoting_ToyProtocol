# Electronic Voting Protocol with Anamorphic ElGamal Encryption

---

This toy protocol for electronic voting addresses the issue of vote buying by utilizing 
anamorphic encryption during the voting process. The protocol ensures that the voter's real
vote is concealed within the ciphertext, while the fake vote (cast by the vote buyer) is 
treated as a regular message. This approach allows the user to cast their vote for the genuine
candidate, while simultaneously providing proof to the vote buyer that they voted for the desired
candidate. The program levarages the ElGamal Anamorphic Extension, as described in the paper Anamorphic Encryption,
Revisited by Fabio Banfi et al. 

--- 

## Notes

1. **Simplified implementation**: This is a toy version of the protocol, designed for a **single-user mode** with predefined values.
2. **Customization**: Vote values and encryption scheme parameters can be modified directly in the code.

--- 

## Requirements

To run the program, you need the **PyCryptodome** package. You can install it using pip:

    pip install pycryptodome

## Running the Program

Once the dependencies are installed, you can execute the program by running:

    python Execution.py

This will start the voting protocol and initiate the voting process using the ElGamal encryption scheme.

## Testing the program

To run a set of basic tests for the protocol, you can execute the following command:

    python test.py

This will run predefined tests and verify the correctness of the implementation. 



