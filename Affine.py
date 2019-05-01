class NotOneToOneError(Exception):
    pass

class Affine:
    
    def __init__(self, shift, a = 1):
        self.a = a
        self.shift = shift 
        if not Affine.coprime(a, 26):
            raise NotOneToOneError(str(a) + ' and 26 should be coprime in order for the affine cipher to become one-to-one')

    @staticmethod
    def coprime(a, b):
        while b != 0:
            a, b = b, a % b
        return a == 1

    @staticmethod
    def modInverse(a, m):
        a = a % m
        for i in range(1, m):
            if ((a*i) % m == 1):
                return i
        return 1

    def encrypt(self, plain_text):
        plain_text = plain_text.lower()
        cipher_text = str()
        for i in plain_text:
            if ord(i) in range(97, 97+26):
                cipher_text += chr((self.a * (ord(i)%97) + self.shift) % 26 + 97)
            else:
                cipher_text += i
        return cipher_text

    def decrypt(self, cipher_text):
        plain_text = str()
        for i in cipher_text:
            if ord(i) in range(97, 97+26):
                plain_text += chr(Affine.modInverse(self.a, 26) * (ord(i)%97 - self.shift) % 26 + 97)
            else:
                plain_text += i
        return plain_text

    @staticmethod
    def affine_brute_force(cipher):
        possible_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        with open('brute_force.txt', 'w') as file: 
            for a in possible_a:
                for b in range(0, 26):
                    c = Affine(b, a)
                    file.write(str(a) + ';' +str(b) + ';' + c.decrypt(cipher).replace(' ','') + '\n')
                    del c
    
    @staticmethod
    def quadgrams_stats(cipher):
        # todo: optimization
        with open('scores.txt', 'w') as scores_file:
            with open('brute_force.txt', 'r') as file:
                brute_force_lines = file.readlines()
            for line in brute_force_lines:
                a,b,cipher = line.split(';')
                cipher = cipher[:-1]
                cipher1 = cipher
                # print(a + ' ' + b + ' ' + cipher)
                quadgrams_count = dict()
                while cipher:
                    c = cipher[:4]
                    if len(c) < 4:
                        break
                    if c not in quadgrams_count.keys():
                        quadgrams_count[c] = 1
                    else:
                        quadgrams_count[c] += 1
                    cipher = cipher[1:]
                # print(quadgrams_count)
                with open('english_quadgrams.txt', 'r') as file:
                    all_quadgrams_stats = file.readlines()
                score = 0
                for quadgram_stat in all_quadgrams_stats:
                    quad, stat = quadgram_stat.split(' ')
                    quad.strip()
                    quad = quad.lower()
                    stat = int(stat[:-1])
                    # print(quad + ' ' + str(stat))
                    if quadgrams_count.get(quad):
                        score += stat * quadgrams_count[quad]
                        #print(score)
                scores_file.write(a + ';' + b + ';' + cipher1 + ';' + str(score) + '\n')

    @staticmethod
    def get_highest_scores():
        with open('scores.txt', 'r') as file:
            content = file.readlines()
        score_key_cipher = dict()
        for line in content:
            abcipher,sep, score = line.rpartition(';')
            score_key_cipher[int(score[:-1])] = abcipher
        scores = sorted(score_key_cipher, reverse=True)
        print('the first 5 plaintext possibilities: ')
        for score in scores[:5]:
            print('score: ' + str(score), end=' ')
            abcipher = score_key_cipher[score]
            a,b,plain = abcipher.split(';')
            print('a= ' + a + ' b= ' + b + ' plaintext= ' + plain)
        
if __name__ == "__main__":
    # plain = 'meet me after the yoga party' 
    # c = Affine(5, a=11)    
    # cipher = c.encrypt(plain)
    # print(cipher)
    # print(c.decrypt(cipher))
    cipher = 'hxxg hx figxk gex jdtf ofkgj'
    Affine.affine_brute_force(cipher)
    Affine.quadgrams_stats(cipher)
    Affine.get_highest_scores()