import random
import collections
from typing import Callable, Dict, List, Tuple, TypeVar
import weakref
from collections import Counter

from util import *

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]


############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction


def extractWordFeatures(x: str) -> FeatureVector:
    """
    Extrae características de palabras para una cadena x. Las palabras
    son delimitadas por espacios en blanco unicamente.
    @param string x:
    @return dict: representación en vector de características de x.
    Ejemplo: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # Inicio de tu código
    words = x.split(" ")
    feature_vector = {}
    
    for word in words:
    	if word in feature_vector:
    	    feature_vector[word] += 1
    	else:
    		feature_vector[word] = 1
    	
    return feature_vector
   
    # Fin de tu código

############################################################
# Problem 3b: stochastic gradient descent

T = TypeVar("T")


def learnPredictor(
    trainExamples: List[Tuple[T, int]],
    validationExamples: List[Tuple[T, int]],
    featureExtractor: Callable[[T], FeatureVector],
    numEpochs: int,
    eta: float,
) -> WeightVector:
    """
    A partir de |trainExamples| y |validationExamples| (cada uno siendo una lista
    de parejas (x,y)), un |featureExtractor| para aplicar a x, y el número de
    épocas para entrenar |numEpochs|, el tamaño de paso |eta|, regresa el vector
    de pesos (vector de características disperas) aprendido.

    Debes implementar descenso de gradiente estocástico.

    Notas:
    - ¡Solo usa trainExamples para entrenar!
    - Debes llamar evaluatePredictor() sobre trainExamples y validationExamples para
    ver cómo te está llendo conforme aprendes después de cada época.
    - El predictor debe tener como salida +1 si el puntaje es precisamente 0.
    """
    weights = {}  # característica => peso

    # Inicio de tu código
    for epoch in range(numEpochs):
        for example, label in trainExamples:
            features = featureExtractor(example)
            
            gradiente = gradient_loss(weights,features,label)

            weights

            if gradiente ==0:
                weights = weights
            else:
                weights = resta_vectores(weights, multiply_dict_values(gradiente,eta))
            
        error_train = evaluatePredictor(trainExamples,lambda x: (
            1 if dotProduct(weights, featureExtractor(x)) >= 0 else -1))
        error_validation = evaluatePredictor(validationExamples,lambda x: (
            1 if dotProduct(weights, featureExtractor(x)) >= 0 else -1))
    
    print(f"Epoch {epoch}: train error = {error_train:.10f}, validation error = {error_validation:.10f}")
    # Fin de tu código

    return weights


############################################################
# Problem 3c: generate test case


def generateDataset(numExamples: int, weights: WeightVector) -> List[Example]:
    """
    Regresa un conjunto de ejemplos (phi(x), y) aleatoriamente que sean clasificados
    correctamente por |weights|.
    """
    random.seed(42)

    # Regresa un solo ejemplo (phi(x), y).
    # phi(x) debe ser un diccionario cuyas llaves sean un subconjunto de las
    # llaves en weights y los valores pueden ser cualquier cosa con un puntaje
    # para el vector de pesos dado.
    # y debe ser 1 o -1 como lo clasifica el vector de pesos.
    # y debe ser 1 si el puntaje es precisamente 0.

    # Nota que el vector de pesos puede ser arbitrario durante las pruebas.
    def generateExample() -> Tuple[Dict[str, int], int]:
        # Inicio de tu código
        phi = {feature: random.random() for feature in random.sample(list(weights), random.randint(0,len(weights)))}
        y = 1 if dotProduct(weights, phi) >=0 else -1
        # Fin de tu código
        return phi, y

    return [generateExample() for _ in range(numExamples)]


############################################################
# Problem 3d: character features


def extractCharacterFeatures(n: int) -> Callable[[str], FeatureVector]:
    """
    Regresa una función que tome una cadena |x| y regrese un vector de
    características disperso que consiste de todos los n-gramas de |x| sin
    espacios asociados a los conteos de n-gramas.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    Puedes suponer que n >= 1.
    """

    def extract(x: str) -> Dict[str, int]:
        # Inicio de tu código
        x = x.replace(" ","") #Sustituimos los espacios.
        engramas = [x[i:i+n] for i in range(len(x)-n+1)]
        return dict (Counter(engramas))
        # Fin de tu código

    return extract


############################################################
# Problem 3e:


def testValuesOfN(n: int):
    """
    Usa este código para probar distintos valores de n para extractCharacterFeatures
    Este código es exclusivo para las pruebas.
    Tu solución escrita completa debe estar en el archivo PDF.
    """
    trainExamples = readExamples("polarity.train")
    validationExamples = readExamples("polarity.dev")
    featureExtractor = extractCharacterFeatures(n)
    weights = learnPredictor(
        trainExamples, validationExamples, featureExtractor, numEpochs=20, eta=0.01
    )
    outputWeights(weights, "weights")
    outputErrorAnalysis(
        validationExamples, featureExtractor, weights, "error-analysis"
    )  # Usa esto para depurar
    trainError = evaluatePredictor(
        trainExamples,
        lambda x: (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1),
    )
    validationError = evaluatePredictor(
        validationExamples,
        lambda x: (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1),
    )
    print(
        (
            "Official: train error = %s, validation error = %s"
            % (trainError, validationError)
        )
    )



############################################################
# Problem 5: k-means
############################################################


def kmeans(
    examples: List[Dict[str, float]], K: int, maxEpochs: int
) -> Tuple[List, List, float]:
    """
    Realiza agrupamiento con K-medias sobre |examples|, donde cada ejemplo es un vector de
    características disperso.

    examples: lista de ejemplos, cada ejemplo es un diccionario string=>float representando un
              un vector disperso.
    K: número de grupos deseados. Supón que 0 < K <= |examples|.
    maxEpochs: máximo número de epocas para correr (debes terminar temprano solo si el algoritmo converge).
    Return: (lista de longitud K de centroides del agrupamiento,
             lista de asignaciones (es decir, si examples[i] pertenece a centers[j], entonces assignments[i] = j),
             pérdida final)
    """
    # Inicio de tu código
    def distance(x, mu):
        return sum((x[i] - mu[i])**2 for i in x)

    centers = random.sample(examples, K)
    z = [0] * len(examples)
    for t in range(maxEpochs):
        # step 1
        for i, x in enumerate(examples):
            min_d = 1000000000
            for k, mu in enumerate(centers):
                d = distance(x, mu)
                if d < min_d:
                    min_d = d
                    z[i] = k
        # step 2
        for k, mu in enumerate(centers):
            sum_x = collections.defaultdict(float)
            count = z.count(k)
            for i, x in enumerate(examples):
                if z[i] == k:
                    increment(sum_x, 1 / count, x)
                centers[k] = sum_x
    # calculate loss
    loss = 0
    for i, x in enumerate(examples):
        diff = x.copy()
        increment(diff, -1, centers[z[i]])
        loss += dotProduct(diff, diff)

    return (centers, z, loss)
    # Fin de tu código
