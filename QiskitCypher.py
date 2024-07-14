from qiskit import QuantumCircuit, execute, Aer
from qiskit.providers.aer.library import SaveExpectationValue
from cryptography.fernet import Fernet

# Function to generate a random key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a message using a key
def encrypt(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Function to create a superposition of all possible keys
def create_superposition(circuit, key_length):
    for i in range(key_length):
        circuit.h(i)

# Function to apply controlled-X gates to encode the ciphertext
def encode_ciphertext(circuit, ciphertext, key_length):
    for i in range(key_length):
        for j in range(key_length):
            if ciphertext[i] == '1' and ciphertext[j] == '1':
                circuit.cx(i, j)

# Function to measure the qubits and obtain the key
def measure_key(circuit, key_length):
    for i in range(key_length):
        circuit.measure(i, i)

# Generate a random key and encrypt a message
original_message = "I am the QiskitCypher message."
key = generate_key()
encrypted_message = encrypt(original_message, key)

# Create a quantum circuit with enough qubits to represent the key
key_length = 8  # For example, AES-128 bit key has a length of 16 bytes or 8 qubits
circuit = QuantumCircuit(key_length)

# Create a superposition of all possible keys
create_superposition(circuit, key_length)

# Encode the ciphertext onto the circuit
ciphertext = bin(int.from_bytes(encrypted_message, 'big'))[2:].zfill(key_length * 8)
encode_ciphertext(circuit, ciphertext, key_length)

# Measure the qubits to obtain the key
measure_key(circuit, key_length)

# Execute the circuit and get the measurement results
simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, simulator).result()
measurement = result.get_counts()

# Convert the measurement results back to a byte string
key_bits = max(measurement, key=lambda item: item[1])
key_bytes = int(key_bits, 2).to_bytes(length=key_length, byteorder='big')

# Decrypt the message using the obtained key
obtained_key = key_bytes
obtained_fernet = Fernet(obtained_key)
decrypted_message = obtained_fernet.decrypt(encrypted_message)

print(f"Original Message: {original_message}")
print(f"Encrypted Message: {encrypted_message}")
print(f"Decrypted Message: {decrypted_message.decode()}")
