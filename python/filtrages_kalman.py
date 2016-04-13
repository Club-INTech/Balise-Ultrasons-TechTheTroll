# -*- coding: utf-8 -*-

from conversion_mesure_etat import *
from math import sqrt
import collections
import scipy.linalg
import generateur_chemin
from structures import Point, Velocity
___author__ = "spraakforskaren"

"""
class Simulator:
    def __init__(self, sizeTableX, sizeTableY):
        self.convertisseur = Convertisseur()

    def add_noise_to_real_position(self, x_reel, y_reel, var):
        x_reel +=  np.random.randn()*var
        y_reel += np.random.randn()*var
        m1, m2, m3 = self.convertisseur.obtenir_mesures(x_reel, y_reel)
        return np.matrix([m1, m2, m3])

    def add_noise_to_sensor_measures(self, x_reel, y_reel, var):
        m1, m2, m3 = self.convertisseur.obtenir_mesures(x_reel, y_reel)
        m1, m2, m3 = m1 + np.random.randn()*var, m2 + np.random.randn()*var, m3 + np.random.randn()*var
        return np.matrix([m1, m2, m3])

    def simuler1(self, x_reel, y_reel, var):

        # Cette simulation prend la position réelle, bruite les mesures et les convertit pour obtenir les positions possibles

        m1, m2, m3 = self.add_noise_to_sensor_measures(x_reel, y_reel, var)
        res = []
        res.append(self.convertisseur.equation1_1_2(m1, m2))
        res.append(self.convertisseur.equation2_1_2(m1, m2))
        res.append(self.convertisseur.equation1_2_3(m2, m3))
        res.append(self.convertisseur.equation2_2_3(m2, m3))
        res.append(self.convertisseur.equation1_3_1(m3, m1))
        res.append(self.convertisseur.equation2_3_1(m3, m1))
        return res

    def simuler2(self, x_reel, y_reel, var):

        # Cette simulation prend la position réelle, bruite les mesures et les convertit pour obtenir les positions possibles

        m1, m2, m3 = self.convertisseur.obtenir_mesures(x_reel, y_reel)
        m1, m2, m3 = m1 + np.random.randn()*var, m2 + np.random.randn()*var, m3 + np.random.randn()*var
        res = []
        res.append(self.convertisseur.equation1_1_2(m1, m2))
        res.append(self.convertisseur.equation2_1_2(m1, m2))
        res.append(self.convertisseur.equation1_2_3(m2, m3))
        res.append(self.convertisseur.equation2_2_3(m2, m3))
        res.append(self.convertisseur.equation1_3_1(m3, m1))
        res.append(self.convertisseur.equation2_3_1(m3, m1))
        return res
    def simuler2(self, x_reel, y_reel, var):

        #Cette simulation prend la position réelle, convertit les mesures, et bruite les positions

        m1, m2, m3 = self.convertisseur.obtenir_mesures(x_reel, y_reel)
        res = []
        res.append(self.convertisseur.equation1_1_2(m1, m2))
        res.append(self.convertisseur.equation2_1_2(m1, m2))
        res.append(self.convertisseur.equation1_2_3(m2, m3))
        res.append(self.convertisseur.equation2_2_3(m2, m3))
        res.append(self.convertisseur.equation1_3_1(m3, m1))
        res.append(self.convertisseur.equation2_3_1(m3, m1))
        return [(conv[0]+ np.dot(np.random.randn(),var), conv[1] + np.dot(np.random.randn(),var)) for conv in res]

    def __compute_velocity(self, x1, y1, x2, y2, duree):
        return np.matrix([(x2-x1)/duree, (y2-y1)/duree])

    def main(self, positions, duree):
        for posi in positions:
            #Vec2 p_bruit = laser.position_balise(balise.id);
            #prévoir le cas où il manque une donnée
            filtrage_lu = FiltrageLaserUnscented(posi)

            #vitesse = self.__compute_velocity(x1, y1, x2, y2, duree)
            # Mise à jour du modèle de filtrage
            vecteur_mesure = np.concatenate([posi, ])
            filtrage_lu.update(vecteur_mesure)
            # Récupération des valeurs filtrées
            p_filtre = filtrage_lu.position()

            #Vérification si l'obstacle est sur la table
            if p_filtre.x > -self.sizeTableX/2 and p_filtre.y > 0 and p_filtre.x < self.sizeTableX/2 and p_filtre.y < self.sizeTableY:
                print "sur la table"
"""
class UnscentedKalman:
    """
       Cette classe implémente l'algorithme du Filitrage de Kalman Unscented
    Source : Machine Learning a probabilistic perspective p. 651-652
    """
    def __init__(self, mu0, SIGMA0, Q, R, d, alpha=2., beta=2., kappa=0., dt=0.25):
        """
        g est la fonction qui associe la position en t à la position en t+1
        h est la fonction qui associe la position réelle aux mesures correspondantes
        mu0 est la position initiale du robot
        SIGMA est la matrice de covariance initiale
        
        """
        self.dt = dt
        self.d = d # c'est la dimension de l'espace cachée 
        self.alpha = float(alpha) #paramètre bizarre
        self.beta = float(beta)  #paramètre bizarre
        self.kappa = kappa  #paramètre bizarre
        self.mu = mu0 #position initiale
        self.SIGMA = SIGMA0 #variance initiale
        self.lam = alpha**2*(d+kappa) - d # un paramètre un peu étrange aussi
        self.gamma = sqrt(d+self.lam) #à nouveau bizarre !
        self.Q = Q # matrice de covariance de la gaussienne de l'équation d'évolution
        self.R = R #matrice de covariance de la gaussienne de l'équation d'observation

        #calculs de coefficients
        self.wm0 = float(self.lam) /(self.d+self.lam)
        self.wm = 1/(2.*(self.d+self.lam))  #wm = wc (wc non implémenté)
        self.wc0 = self.wm0+(1-self.alpha**2+self.beta)
        print self.SIGMA


    def _first_step(self):
        """
        Estimation de mu_barre et de sigma_barre à partir de l'itération précédente
        """
        #first Unscented transform
        racine_sigma = np.asmatrix(scipy.linalg.sqrtm(self.SIGMA))

        # print "racine carrée", racine_sigma
        # print "mu", self.mu#, "racine_sigma", racine_sigma.shape, racine_sigma[:, 1].shape

        self.points_sigma = [self.mu]
        self.points_sigma.extend([self.mu - self.gamma*racine_sigma[:, i] for i in range(0, self.d)]) #de -1 à - self.d
        self.points_sigma.extend([self.mu + self.gamma * racine_sigma[:, i] for i in range(0, self.d)]) # de 1 à self.d

        #print "self.points_sigma", len(self.points_sigma), np.array(self.points_sigma).shape
        #self.points_sigma = np.array(self.points_sigma)
        #self.z_etoile_barre = np.array([self.g(self.points_sigma[i]).reshape((4,)) for i in range(0, 2*self.d)])

        self.z_etoile_barre = []  #np.asmatrix(np.zeros(self.points_sigma.shape))
        # print len(self.points_sigma)
        for i in range(len(self.points_sigma)):
            self.z_etoile_barre.append(self.g(self.points_sigma[i]))
            #self.z_etoile_barre[i,:] = self.g(self.points_sigma[i])

        self.mu_barre = self.wm0*self.z_etoile_barre[0]

        #print "mu_barre", self.mu_barre.shape

        for i in range(1, len(self.z_etoile_barre)):
            #print "self.wm*self.z_etoile_barre[i]", (self.wm*self.z_etoile_barre[i]).shape
            self.mu_barre += self.wm*self.z_etoile_barre[i]

        #calcul de SIGMA_barre
        #print "mu barre", self.mu_barre.shape
        # print "z_etoile_barre", len(self.z_etoile_barre), len(self.z_etoile_barre[0]), self.z_etoile_barre[0], self.mu_barre
        self.SIGMA_barre = self.wc0*np.dot((self.z_etoile_barre[0] - self.mu_barre),
                                                (self.z_etoile_barre[0] - self.mu_barre).T)
        for i in range(1, len(self.z_etoile_barre)):
            self.SIGMA_barre += self.wm*np.dot((self.z_etoile_barre[i] - self.mu_barre),
                                               (self.z_etoile_barre[i] - self.mu_barre).T)
        # print "SIGMA_barre", self.SIGMA_barre.shape
        self.SIGMA_barre += self.Q

    def _second_step(self, y):
        """
        y est la mesure à l'instant t
        Estimation de mu et de sigma présent
        """
        #second unscented transform
        racine_sigma_barre = np.asmatrix(scipy.linalg.sqrtm(self.SIGMA_barre))
        self.points_sigma_barre = [self.mu_barre]+[self.mu_barre - self.gamma*racine_sigma_barre[:, i]
                 for i in range(0, self.d)]+[self.mu_barre + self.gamma * racine_sigma_barre[:, i] for i in range(0, self.d)]
        # print "points_sigma_barre", self.points_sigma_barre
        self.y_etoile_barre = [self.h(self.points_sigma_barre[i]) for i in range(0, len(self.points_sigma_barre))]

        self.y_chapeau = self.wm0*self.y_etoile_barre[0]
        for i in range(1, len(self.y_etoile_barre)):
            self.y_chapeau += self.wm*self.y_etoile_barre[i]
        #Calcul de S
        self.S = self.wc0*np.dot((self.y_etoile_barre[0] - self.y_chapeau),
                                 (self.y_etoile_barre[0] - self.y_chapeau).T)
        for i in range(1, len(self.y_etoile_barre)):
            self.S += self.wm*np.dot((self.y_etoile_barre[i] - self.y_chapeau),
                                (self.y_etoile_barre[i] - self.y_chapeau).T)
        # print "S", self.S.shape
        self.S += self.R
        #calcul de SIGMA_z_y
        self.SIGMA_z_y_barre = self.wc0*np.dot((self.z_etoile_barre[0] - self.mu_barre),
                                          (self.y_etoile_barre[0] - self.y_chapeau).T)
        for i in range(1, len(self.z_etoile_barre)):
            self.SIGMA_z_y_barre += self.wm*np.dot((self.z_etoile_barre[i] - self.mu_barre),
                                              (self.y_etoile_barre[i] - self.y_chapeau).T)
        self.K = np.dot(self.SIGMA_z_y_barre, scipy.linalg.inv(self.S))
        #print "K", self.K.shape, "y", y.shape
        #Les valeurs qui nous interessent
        self.mu = self.mu_barre + np.dot(self.K, (y - self.y_chapeau))
        self.SIGMA = self.SIGMA_barre - np.dot(np.dot(self.K, self.S), self.K.T)

    def filter(self, y):
        """
        On sépare les deux pas parce que l'un a besoin d'une mesure tandis que l'autre non
        :param y: c'est la mesure provenant du capteur
        """
        self._first_step()
        if y is None:  # aucune mesure
            self._second_step(self.mu)  # pour l'instant, c'est une proposition, on pourra trouver mieux
        else:
            self._second_step(y)

    def g(self, x, dim=4):
        """
        Pour notre modélisation, on choisit comme vecteur x = [abscisse de la position,
        ordonnée de la position] ou [abscisse de la position,
        ordonnée de la position, abscisse de la vitesse, ordonnées de la vitesse]
        """
        if dim == 2:
            F = np.matrix([[1., 0.], [0., 1.]])
        elif dim == 3:
            F = np.matrix([[1., 0, 0], [0., 1., 0.], [0., 0., 1.]])
        else: #dim == 4
            F = np.matrix([[1., 0., self.dt, 0.], [0., 1., 0., self.dt], [0., 0., 1., 0.], [0., 0., 0., 1.]])
        # print F.shape, x.shape
        res = np.dot(F, x)
        # print res.shape
        return res

    def h(self, x):
        """
        La fonction renvoie les données comme si elles ont été mesurées.
        """
        # print "x shape", x.shape
        conv = Converter()
        measures = conv.get_measures_from_state(x[0],x[1])


        return np.asmatrix(measures).T#[:,np.newaxis]

    def get_state(self):
        """
        self.mu est la position moyenne
        """
        return self.mu


#classe à arranger pour le Kalman Unscented
class UnscentedKalmanFilter:
    
    def __init__(self, x0, dt=0.025, dime=4):
        """
        x0 est un array(x,y) ou array(x,y,x point, y point)
        """
        self.dt = dt
        #x = np.array(x).T
        mu0 = x0
        #x = np.array([1400,100,0.,0.])[:, np.newaxis] # vecteur d'état au départ
        if dime == 2:
            SIGMA0 = np.matrix([[1., 0.], [0., 1.]])
            R = np.matrix([[90, 0., 0.], [0., 90, 0.], [0., 0., 90]])  #dimension de la matrice égale au nombre de dimensions des mesures !
            Q = np.matrix([[self.dt**3/3., 0, self.dt**2/2., 0],[0, self.dt**3/3., 0, self.dt**2/2],
                       [self.dt**2/2., 0, 4*self.dt, 0],[0, self.dt**2/2, 0, 4*self.dt]])
        else:
            SIGMA0 = np.matrix([[0.1, 0., 0., 0.], [0., 0.1, 0., 0.], [0., 0., 0.01, 0.], [0., 0., 0., 0.01]]) # incertitude initiale
            R = np.matrix([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])  #dimension de la matrice égale au nombre de dimensions des mesures !
            R *= 0.01
            #Q = np.matrix([[self.dt**3/3., self.dt**2/2., 0, 0],[self.dt**2/2.,self.dt, 0, 0],
            #            [0,0,self.dt**3/3.,self.dt**2/2],[0,0,self.dt**2/2,self.dt]])
            #Q *= 20;
            Q = np.matrix([[1., 0, 0, 0],[0, 1, 0, 0],
                           [0, 0, 1, 0],[0, 0, 0, 1]])
            # Q = np.matrix([[self.dt**3/3., 0, self.dt**2/2., 0],[0, self.dt**3/3., 0, self.dt**2/2],
            #                [self.dt**2/2., 0, 4*self.dt, 0],[0, self.dt**2/2, 0, 4*self.dt]])
            #Q = np.matrix([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 4, 0],[0, 0, 0, 4]])
            Q *= 0.1
        d = 4
        kappa = 1
        alpha = 0.5
        beta = 1
        self.ukf = UnscentedKalman(mu0, SIGMA0, Q, R, d, alpha=alpha, beta=beta, kappa=kappa)
        self.historique = collections.deque(maxlen=3)
        self.valeurs_rejetees = 0
        self.acceleration = None
        
    def get_state(self):
        """

        :return: the state of the robot
        """
        return self.ukf.mu
        
    def update_dt(self, new_dt):
        """
        Modifie la période d'échantillonage
        """
        self.dt = new_dt
        self.ukf.F[0,2] = new_dt
        self.ukf.F[1,3] = new_dt

    def get_state_position(self):
        """

        :return: a Point
        """
        state = self.ukf.mu
        # print state
        return Point(float(state[0]), float(state[1]))

    def get_state_velocity(self):
        """

        :return: a Velocity
        """
        state = self.ukf.mu
        return Velocity(float(state[2]), float(state[3]))
                
    def update(self, y):
        """
        Je ne sait pas si c'est vraiement utilse
        fonction qui est utilisé à chaque mesure
        y est un vecteur de mesure de dimension 4 : (x, y, x point, y point)
        """

        #if self._filtrage_acceleration(Point(x, y)):
        #    self.last_point = Point(x, y)
        self.ukf.filter(y)
        pos_filtre = self.ukf.get_state()
        #    self.filtre_kalman.measurement(np.array([x,y])[:, np.newaxis])
        self.historique.append(self.ukf.get_state())
        # print y, pos_filtre[0], pos_filtre[1]
        #else:
        #    self.last_point = None
        return pos_filtre
        #    self.filtre_kalman.prediction()
        
    def _acceleration_filtering(self, pointm0):
        """
        Vérifie si le point est cohérent avec la position actuelle, en basant sur l'accélération
        """
        # Pas suffisamment de valeurs précédentes pour calculer l'accélération
        if len(self.historique) != 3:
            return True
            
        # 3 derniers points valides
        pointm1 = self.historique[2]
        pointm2 = self.historique[1]
        pointm3 = self.historique[0]
        
        # Vecteurs vitesses et accélération
        vitesse_actuelle = pointm0 - pointm1
        vitesse_m1 = pointm1 - pointm2
        vitesse_m2 = pointm2 - pointm3
        acceleration_actuelle = vitesse_actuelle - vitesse_m1
        acceleration_precedente = vitesse_m1 - vitesse_m2
        jerk = acceleration_actuelle - acceleration_precedente
        
        # Produit scalaire pour savoir s'il y a accélération ou décélération
        produit = acceleration_actuelle.x * vitesse_m1.x + acceleration_actuelle.y * vitesse_m1.y
        
        # Rejette les accélérations brutales
        if acceleration_actuelle.norme() / self.dt**2 > 50000 and self.valeurs_rejetees < 3:
            #~ print("accélération = {0}, produit = {1}, jerk = {2}".format(acceleration_actuelle.norme() / self.dt**2, produit, jerk.norme() / self.dt**3))
            self.valeurs_rejetees += 1
            return False
        else:
            self.valeurs_rejetees = 0
            return True


class Kalman:
    """
    Classe  qui implémente le filtre de Kalman. Utilisé, il permet de filtrer une suite discrétisé de valeur mesurée
    """
  
    def __init__(self, x, P, F, H, R, Q):
        """
        :param x: Etat initial du truc à suivre (un vecteur position le plus souvent)
        :param P: matrice incertitude sur le modèle d'évolution
        :param F: matrice de transition du modèle d'évolution
        :param H: matrice matrice d'observation
        :param R: matrice de covariance de la mesure
        :param Q: matrice de covariance du modèle

        """
        self.x = x
        self.P = P
        self.F = F
        self.H = H
        self.R = R
        self.Q = Q
  
    def predict(self, u=None):
        """
        C'est la partie prédiction, le modèle imagine comment l'état suivant sera
        :param u: un vecteur "déplacement", si onsait de combien ça a dû bouger, il faut le mettre
        """
        if u is None:
            u = np.zeros(self.x.shape[0])[:, np.newaxis]
        self.x = np.dot(self.F, self.x) + u
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def measure(self, mes):
        """
        C'est la partie où on prend en compte la nouvelle mesure
        :param mes: vecteur de même dimension que x
        """
        y = mes - np.dot(self.H, self.x)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        self.P = np.dot((np.identity(self.x.shape[0]) - np.dot(K, self.H)), self.P)


    def filter(self, mes, u=None):
        """
        Méthode qui condense une étape du filtrage
        """
        self.predict(u)
        self.measure(mes)


class ExtendedKalman:
    """
    Un jour, ça sera fait
    """
    pass
    

class FiltrageKalman:
    """
    Classe qui utilise Kalman
    """
    def __init__(self, x0, dt=0.025):
        """

        :param x0: état initial
        :param dt: pas de la mesure (période d'échantillonage)
        """
        self.dt = dt
        x = x0  #np.array([1400, 100, 0., 0.])[:, np.newaxis] # vecteur d'état au départ
        P = np.matrix([[30.0, 0., 0., 0.], [0., 30., 0., 0.], [0., 0., 10., 0.], [0., 0., 0., 10.]]) # incertitude initiale
        F = np.matrix([[1., 0., self.dt, 0.], [0., 1., 0., self.dt], [0., 0., 1., 0.], [0., 0., 0., 1.]]) # matrice de transition
        H = np.matrix([[1., 0., 0., 0.], [0., 1., 0., 0.]])# matrice d'observation
        R = np.matrix([[900, 0.], [0., 900]]) # incertitude sur la mesure

        #Q = np.matrix([[self.dt**3/3., self.dt**2/2., 0, 0],[self.dt**2/2.,self.dt, 0, 0],
        #            [0,0,self.dt**3/3.,self.dt**2/2],[0,0,self.dt**2/2,self.dt]])
        #Q *= 20;

        Q = np.matrix([[self.dt**3/3., 0, self.dt**2/2., 0],[0, self.dt**3/3., 0, self.dt**2/2], \
                       [self.dt**2/2., 0, 4*self.dt, 0],[0, self.dt**2/2, 0, 4*self.dt]])
        #Q = np.matrix([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 4, 0],[0, 0, 0, 4]])
        Q *= 30
        self.kalman_filter = Kalman(x, P, F, H, R, Q)
        self.history = collections.deque(maxlen=3)
        self.rejected_values = 0
        self.acceleration = None
        
    def get_current_state(self):
        return self.kalman_filter.x

    def get_current_position(self):
        state = self.get_current_state()
        return Point(float(state[0]), float(state[1]))
        
    def update_dt(self, new_dt):
        self.dt = new_dt
        self.kalman_filter.F[0,2] = new_dt
        self.kalman_filter.F[1,3] = new_dt
    
    def get_last_state(self):
        #state = self.filtre_kalman.x
        #return Point(int(state[0]), int(state[1]))
        return self.last_point
    
    # def vitesse(self):
    #     state = self.kalman_filter.x
    #     return Vitesse(int(state[2]), int(state[3]))
                
    def update(self, x, y):
        if self.acceleration_filtering(Point(x, y)):
            self.last_point = Point(x, y)
            self.kalman_filter.predict()
            self.kalman_filter.measure(np.array([x, y])[:, np.newaxis])
            self.history.append(self.get_last_state())
        else:
            self.last_point = None
            self.kalman_filter.predict()
        
    def acceleration_filtering(self, pointm0):
        """
        Vérifie si le point est cohérent avec la position actuelle, en se basant sur l'accélération
        """
        # Pas suffisamment de valeurs précédentes pour calculer l'accélération
        if len(self.history) != 3:
            return True
            
        # 3 derniers points valides
        pointm1 = self.history[2]
        pointm2 = self.history[1]
        pointm3 = self.history[0]
        
        # Vecteurs vitesses et accélération
        vitesse_actuelle = pointm0 - pointm1
        vitesse_m1 = pointm1 - pointm2
        vitesse_m2 = pointm2 - pointm3
        acceleration_actuelle = vitesse_actuelle - vitesse_m1
        acceleration_precedente = vitesse_m1 - vitesse_m2
        jerk = acceleration_actuelle - acceleration_precedente
        
        # Produit scalaire pour savoir s'il y a accélération ou décélération
        produit = acceleration_actuelle.x * vitesse_m1.x + acceleration_actuelle.y * vitesse_m1.y
        
        # Rejette les accélérations brutales
        if acceleration_actuelle.norme() / self.dt**2 > 50000 and self.rejected_values < 3:
            #~ print("accélération = {0}, produit = {1}, jerk = {2}".format(acceleration_actuelle.norme() / self.dt**2, produit, jerk.norme() / self.dt**3))
            self.rejected_values += 1
            return False
        else:
            self.rejected_values = 0
            return True


def get_velocity(positions, dt):
    """

    :param positions: matrice des positions
    :param dt: période d'échantillonage
    :return:
    """
    velocities = np.zeros(positions.shape)
    for i in range(1, velocities.shape[0]):
        velocities[i, :] = (positions[i, :] - positions[i-1, :])/float(dt)
    return velocities


def get_distance(point1, point2):
    """

    :param point1: couple (x,y)
    :param point2: couple (x,y)
    :return:
    """
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def get_mer(real, estimated):
    """
    Renvoie la moyenne des distances
    :param real: liste de couples (x,y)
    :param estimated: liste de couples (x,y)
    :return:
    """
    try:
        res = [real[i].distance(estimated[i]) for i in range(len(real))]
        print "La moyenne des distances entre les estimations et la réalité est : "
        return sum(res)/float(len(res))
    except ValueError:
        print real[i]
        print estimated[i]
    # except IndexError:
    #     print i
    #     print len(real)
    #     print len(estimated)



def squared_error(real_values, filtered_values):
    """
    Renvoie l'erreur quadratique moyenne !
    :param real_values:
    :param filtered_values:
    :return:
    """
    diff = real_values[:, :2] - filtered_values[:, :2]
    res = diff.T.dot(diff)
    "L'erreur quadratique est : "
    return res


def script_unscented_with_real_measures():
    """
    Script utilisant le filtre de Kalman unscented avec des mesures réelles !
    :return:
    """
    measures_pos = np.genfromtxt("mesures_25.txt", delimiter="\t")
    real_path = []
    for i in range(1, measures_pos.shape[0]):
        x = measures_pos[i, 0]
        y = measures_pos[i, 1]
        real_path.append(Point(x, y))
    vite = get_velocity(measures_pos, 0.025)
    measures = np.concatenate((measures_pos, vite), axis=1)
    filtering = UnscentedKalmanFilter(measures[0, :].T, dt=0.025, dime=4)
    var = 10
    l_pos_filter = []
    for i in range(1, measures.shape[0]):
        x = measures[i, 0]
        y = measures[i, 1]
        print "x et y", x, y
        conv = Converter()
        m1, m2, m3 = conv.get_measures_from_state(x, y)
        m1, m2, m3 = m1 + np.random.randn()*var, m2 + np.random.randn()*var, m3 + np.random.randn()*var
        filtering.update(np.asmatrix([m1, m2, m3]).T)
        pos = filtering.get_state_position()
        l_pos_filter.append(pos)
    print "estimée", filtering.get_state_position()
    print "vraie", measures[measures.shape[0]-1, :]
    # print erreur_quadratique(measures, np.asmatrix(np.array(l_pos_filtre)))
    print len(real_path), len(l_pos_filter), measures.shape[0]
    print get_mer(real_path, l_pos_filter)


def script_classic_trajectory_with_real_measures():
    """
    Script utilisant le filtre de Kalman  avec des mesures réelles !
    :return:
    """
    dt=0.025
    print "trajectoire"
    measures_pos = np.genfromtxt("mesures_25.txt", delimiter="\t")
    real_path = []
    for i in range(measures_pos.shape[0]):
        x = measures_pos[i, 0]
        y = measures_pos[i, 1]
        real_path.append(Point(x, y))

    l_pos_filtre = [real_path[0]]
    print "mesures", measures_pos.shape
    print "créée"
    vite = get_velocity(measures_pos, dt)
    measures = np.concatenate((measures_pos, vite), axis=1)
    measures = np.asmatrix(measures)
    print measures.shape
    filtering = FiltrageKalman(measures[0, :].T, dt=dt)
    var = 10
    for i in range(1, measures.shape[0]):
        x = measures[i, 0]
        y = measures[i, 1]
        # print "x et y", x, y, "i" ,i
        x_bruite, y_bruite = x + np.random.randn()*var, y + np.random.randn()*var
        filtering.update(x_bruite, y_bruite)
        pos = filtering.get_current_position()
        l_pos_filtre.append(pos)
    print "bruitée", x_bruite, y_bruite
    print "estimée", filtering.get_current_state()
    print "vraie", measures[measures.shape[0]-1, :]
    # print erreur_quadratique(measures, np.asmatrix(np.array(l_pos_filtre)))
    print get_mer(real_path, l_pos_filtre)


def script_classic_trajectory():
    """
    Script utilisant le filtre de Kalman  avec des mesures simulées à partir d'une trajectoire inventée !
    :return:
    """
    print "trajectoire"
    l_points = [[-1000., 200.], [-1000., 800.], [-400., 1200.], [500., 500.], [1100., 180.]]
    dt = 0.025
    real_path = generateur_chemin.generate_path(l_points=l_points, velocity_translation=25,
                                                            velocity_rotation=0.7, dt=dt)
    measures_pos = np.array(real_path)
    x, y = real_path[0]
    l_pos_filtre = [Point(x, y)]
    print "mesures", measures_pos.shape
    print "créée"
    vite = get_velocity(measures_pos, dt)
    measures = np.concatenate((measures_pos, vite), axis=1)
    measures = np.asmatrix(measures)
    print measures.shape
    filtering = FiltrageKalman(measures[0, :].T, dt=dt)
    var = 10
    for i in range(1, measures.shape[0]):
        x = measures[i, 0]
        y = measures[i, 1]
        # print "x et y", x, y, "i" ,i
        x_bruite, y_bruite = x + np.random.randn()*var, y + np.random.randn()*var
        filtering.update(x_bruite, y_bruite)
        pos = filtering.get_current_position()
        l_pos_filtre.append(pos)
    print "bruitée", x_bruite, y_bruite
    print "estimée", filtering.get_current_position()
    print "vraie", measures[measures.shape[0]-1, :]
    # print erreur_quadratique(measures, np.asmatrix(np.array(l_pos_filtre)))
    print get_mer(real_path, l_pos_filtre)


def script_unscented_trajectory():
    """
    Script utilisant le filtre de Kalman unscented avec des mesures simulées à partir d'une trajectoire inventée !
    :return:
    """
    print "trajectoire"
    l_points = [[-1000., 200.], [-1000., 800.], [-400., 1200.], [500., 500.], [1100., 180.]]
    dt = 0.025
    real_path = generateur_chemin.generate_path(l_points=l_points, velocity_translation=25,
                                                            velocity_rotation=0.7, dt=dt)
    x, y = real_path[0]
    l_pos_filter = [Point(x, y)]
    measures_pos = np.array(real_path)

    print "mesures", measures_pos.shape
    print "créée"
    vite = get_velocity(measures_pos, dt)
    measures_pos = np.concatenate((measures_pos, vite), axis=1)
    measures_pos = np.asmatrix(measures_pos)

    filtering = UnscentedKalmanFilter(measures_pos[0l, :].T, dt=dt, dime=4)
    var = 10
    for i in range(1, measures_pos.shape[0]):
        x = measures_pos[i, 0]
        y = measures_pos[i, 1]
        # print "x et y", x, y, "i", i
        conv = Converter()
        m1, m2, m3 = conv.get_measures_from_state(x, y)
        m1, m2, m3 = m1 + np.random.randn()*var, m2 + np.random.randn()*var, m3 + np.random.randn()*var
        filtering.update(np.asmatrix([m1, m2, m3]).T)
        l_pos_filter.append(filtering.get_state_position())
    print "estimée", filtering.get_state_position()
    print "vraie", measures_pos[measures_pos.shape[0]-1, :]
    # print erreur_quadratique(measures, np.asmatrix(np.array(l_pos_filtre)))
    print get_mer(real_path, l_pos_filter)


def script_unscented_with_fake_ultrasound_measures():
    dt = 0.025
    print "trajectoire"
    measures_pos = np.genfromtxt("mesures_25.txt", delimiter="\t")
    real_path = []
    for i in range(1, measures_pos.shape[0]):
        x = measures_pos[i, 0]
        y = measures_pos[i, 1]
        real_path.append(Point(x, y))
    print measures_pos[0, :].shape
    print measures_pos[0, :]
    l_pos_filter = [Point(measures_pos[0, :][0], measures_pos[0, :][1])]
    vite = get_velocity(measures_pos, dt)
    measures_pos = np.concatenate((measures_pos, vite), axis=1)
    measures_pos = np.asmatrix(measures_pos)

    measures_us = np.genfromtxt("mesures_25_sigma10.txt", delimiter=",")


    print "mesures", measures_pos.shape
    print "créée", measures_us.shape
    filtering = UnscentedKalmanFilter(measures_pos[0, :].T, dt=dt)
    # var = 10
    for i in range(1, measures_us.shape[0]):
        # print measures_us[i, :].shape
        m1 = measures_us[i, 0]
        m2 = measures_us[i, 1]
        m3 = measures_us[i, 2]
        # print "x et y", x, y, "i" ,i
        filtering.update(np.asmatrix([m1, m2, m3]).T)
        pos = filtering.get_state_position()
        l_pos_filter.append(pos)
    # print "bruitée", x_bruite, y_bruite
    print "estimée", filtering.get_state_position()
    print "vraie", measures_pos[measures_pos.shape[0]-1, :]
    # print erreur_quadratique(measures, np.asmatrix(np.array(l_pos_filtre)))
    print get_mer(real_path, l_pos_filter)


if __name__ == "__main__":
    # script_unscented_with_real_measures()
    # script_unscented_trajectory()
    script_classic_trajectory()
    # script_classic_trajectory_with_real_measures()
    # script_unscented_with_fake_ultrasound_measures()