#-*- coding: utf-8 -*-

from bruitage_conversion import *
from math import sqrt
import collections
import scipy.linalg

class Simulator:
    def __init__(self, sizeTableX, sizeTableY):
        self.convertisseur = Convertisseur()
        self.sizeTableX = sizeTableX
        self.sizeTableY = sizeTableY
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
        """
        Cette simulation prend la position réelle, bruite les mesures et les convertit pour obtenir les positions possibles
        """
        m1, m2, m3 = self.add_noise_to_sensor_measures(x_reel, y_reel, var)
        res = []
        res.append(self.convertisseur.equation1_1_2(m1, m2))
        res.append(self.convertisseur.equation2_1_2(m1, m2))
        res.append(self.convertisseur.equation1_2_3(m2, m3))
        res.append(self.convertisseur.equation2_2_3(m2, m3))
        res.append(self.convertisseur.equation1_3_1(m3, m1))
        res.append(self.convertisseur.equation2_3_1(m3, m1))
        return res
    def simuler1(self, x_reel, y_reel, var):
        """
        Cette simulation prend la position réelle, bruite les mesures et les convertit pour obtenir les positions possibles
        """
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
        """
        Cette simulation prend la position réelle, convertit les mesures, et bruite les positions
        """
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
        #print self.mu, "self.mu"
        self.SIGMA = SIGMA0 #variance initiale
        self.lam = alpha**2*(d+kappa) - d # un paramètre un peu étrange aussi
        self.gamma = sqrt(d+self.lam) #à nouveau bizarre !
        self.Q = Q # matrice de covariance de la gaussienne de l'équation d'évolution
        self.R = R #matrice de covariance de la gaussienne de l'équation d'observation

        #calculs de coefficients
        self.wm0 = self.lam /(self.d+self.lam)
        self.wm = 1/(2.*(self.d+self.lam))  #wm = wc (wc non implémenté)
        self.wc0 = self.wm0+(1-self.alpha**2+self.beta)

    def _first_step(self):
        """
        Estimation de mu_barre et de sigma_barre à partir de l'itération précédente
        """
        #first Unscented transform
        #racine_sigma = scipy.linalg.sqrtm(self.SIGMA)
        racine_sigma = np.asmatrix(scipy.linalg.sqrtm(self.SIGMA))
        print "racine carrée", racine_sigma
        print "mu", self.mu#, "racine_sigma", racine_sigma.shape, racine_sigma[:, 1].shape
        self.points_sigma = [self.mu]
        self.points_sigma.extend([self.mu - self.gamma*racine_sigma[:, i] for i in range(0, self.d)]) #de -1 à - self.d
        self.points_sigma.extend([self.mu + self.gamma * racine_sigma[:, i] for i in range(0, self.d)]) # de 1 à self.d
        #print "self.points_sigma", len(self.points_sigma), np.array(self.points_sigma).shape
        #self.points_sigma = np.array(self.points_sigma)
        #self.z_etoile_barre = np.array([self.g(self.points_sigma[i]).reshape((4,)) for i in range(0, 2*self.d)])
        self.z_etoile_barre = []  #np.asmatrix(np.zeros(self.points_sigma.shape))
        for i in range(0, 2*self.d):
            self.z_etoile_barre.append(self.g(self.points_sigma[i]))
            #self.z_etoile_barre[i,:] = self.g(self.points_sigma[i])

        self.mu_barre = self.wm0*self.z_etoile_barre[0]
        #print "mu_barre", self.mu_barre.shape
        for i in range(1, 2*self.d):
            #print "self.wm*self.z_etoile_barre[i]", (self.wm*self.z_etoile_barre[i]).shape
            self.mu_barre += self.wm*self.z_etoile_barre[i]
        #calcul de SIGMA_barre
        #print "mu barre", self.mu_barre.shape
        print "z_etoile_barre", len(self.z_etoile_barre), len(self.z_etoile_barre[0]), self.z_etoile_barre[0], self.mu_barre
        self.SIGMA_barre = self.wc0*np.dot((self.z_etoile_barre[0] - self.mu_barre),
                                                (self.z_etoile_barre[0] - self.mu_barre).T)
        for i in range(1,2*self.d):
            self.SIGMA_barre += self.wm*np.dot((self.z_etoile_barre[i] - self.mu_barre),
                                               (self.z_etoile_barre[i] - self.mu_barre).T)
        print "SIGMA_barre", self.SIGMA_barre.shape
        self.SIGMA_barre += self.Q

    def _second_step(self, y):
        """
        y est la mesure à l'instant t
        Estimation de mu et de sigma présent
        """
        #second unscented transform
        racine_sigma = np.asmatrix(scipy.linalg.sqrtm(self.SIGMA_barre))
        self.points_sigma_barre = [self.mu_barre]+[self.mu - self.gamma*racine_sigma[:, i]
                 for i in range(0,self.d)]+[self.mu_barre + self.gamma * racine_sigma[:, i] for i in range(0, self.d)]
        print "points_sigma_barre", self.points_sigma_barre
        self.y_etoile_barre = [self.h(self.points_sigma_barre[i]) for i in range(0, 2*self.d)]

        self.y_chapeau = self.wm0*self.y_etoile_barre[0]
        for i in range(1, 2*self.d):
            self.y_chapeau += self.wm*self.y_etoile_barre[i]
        #Calcul de S
        self.S = self.wc0*np.dot((self.y_etoile_barre[0] - self.y_chapeau),
                                 (self.y_etoile_barre[0] - self.y_chapeau).T)
        for i in range(1,2*self.d):
            self.S += self.wm*np.dot((self.y_etoile_barre[i] - self.y_chapeau),
                                (self.y_etoile_barre[i] - self.y_chapeau).T)
        print "S", self.S.shape
        self.S += self.R
        #calcul de SIGMA_z_y
        self.SIGMA_z_y_barre = self.wc0*np.dot((self.z_etoile_barre[0] - self.mu_barre),
                                          (self.y_etoile_barre[0] - self.y_chapeau).T)
        for i in range(1, 2*self.d):
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
        """
        self._first_step()
        if y is None: #aucune mesure
            self._second_step(self.mu) #pout l'instant, c'est une proposition, on pourra trouver mieux
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
        else: #dim == 4
            F = np.matrix([[1., 0., self.dt, 0.], [0., 1., 0., self.dt], [0., 0., 1., 0.], [0., 0., 0., 1.]])
        print F.shape, x.shape
        res = np.dot(F, x)
        print res.shape
        return res

    def h(self, x):
        """
        La fonction renvoie les données comme si elles ont été mesurées.
        """
        print "x shape", x.shape
        a = Convertisseur()

        return np.asmatrix(a.obtenir_mesures(x[0],x[1])).T#[:,np.newaxis]

    def get_position(self):
        """
        self.mu est la position moyenne
        """
        return self.mu


#classe à arranger pour le Kalman Unscented
class FiltrageLaserUnscented:
    
    def __init__(self, x0, dt=0.25, dime=4):
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
            #Q = np.matrix([[self.dt**3/3., self.dt**2/2., 0, 0],[self.dt**2/2.,self.dt, 0, 0],
            #            [0,0,self.dt**3/3.,self.dt**2/2],[0,0,self.dt**2/2,self.dt]])
            #Q *= 20;
            Q = np.matrix([[self.dt**3/3., 0, self.dt**2/2., 0],[0, self.dt**3/3., 0, self.dt**2/2],
                           [self.dt**2/2., 0, 4*self.dt, 0],[0, self.dt**2/2, 0, 4*self.dt]])
            #Q = np.matrix([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 4, 0],[0, 0, 0, 4]])
            Q *= 1
        d = 4
        kappa = 1
        alpha = 0.5
        beta = 1
        self.ukf = UnscentedKalman(mu0, SIGMA0, Q, R, d, alpha=alpha, beta=beta, kappa=kappa)
        self.historique = collections.deque(maxlen=3)
        self.valeurs_rejetees = 0
        self.acceleration = None
        
    def get_state_adverse_robot(self):
        return self.ukf.mu
        
    def update_dt(self, new_dt):
        """
        Modifie la période d'échantillonage
        """
        self.dt = new_dt
        self.ukf.F[0,2] = new_dt
        self.ukf.F[1,3] = new_dt

    def get_position_adverse_robot(self):
        state = self.ukf.mu
        return Point(float(state[0]), float(state[1]))

    def get_velocity_adverse_robot(self):
        state = self.ukf.mu
        return Vitesse(float(state[2]), float(state[3]))
                
    def update(self, y):
        """
        Je ne sait pas si c'est vraiement utilse
        fonction qui est utilisé à chaque mesure
        y est un vecteur de mesure de dimension 4 : (x, y, x point, y point)
        """

        #if self._filtrage_acceleration(Point(x, y)):
        #    self.last_point = Point(x, y)
        self.ukf.filter(y)
        pos_filtre = self.ukf.get_position()
        #    self.filtre_kalman.measurement(np.array([x,y])[:, np.newaxis])
        self.historique.append(self.ukf.get_position())
        print y, pos_filtre[0], pos_filtre[1]
        #else:
        #    self.last_point = None
        #    self.filtre_kalman.prediction()
        
    def _filtrage_acceleration(self, pointm0):
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
  
  def __init__(self,x,P,F,H,R,Q):
    self.x = x
    self.P = P
    self.F = F
    self.H = H
    self.R = R
    self.Q = Q
  
  def prediction(self, u = None):
    if u == None:
        u = np.zeros(self.x.shape[0])[:, np.newaxis]
    self.x = np.dot(self.F, self.x) + u
    self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
  
  def mesure(self, Z):
    y = Z - np.dot(self.H, self.x)
    S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R    
    K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
    self.x = self.x + np.dot(K, y)
    self.P = np.dot((np.identity(self.x.shape[0]) - np.dot(K, self.H)), self.P)

    
  def filtrer(self, Z, u = None):
    self.prediction(u)
    self.mesure(Z)


class ExtendedKalman:
    pass
    

class FiltrageLaser:
    
    def __init__(self):
        self.dt = 0.2
        x = np.array([1400, 100, 0., 0.])[:, np.newaxis] # vecteur d'état au départ
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
        self.filtre_kalman = Kalman(x, P, F, H, R, Q)
        self.historique = collections.deque(maxlen=3)
        self.valeurs_rejetees = 0
        self.acceleration = None
        
    def etat_robot_adverse(self):
        return self.filtre_kalman.x
        
    def update_dt(self, new_dt):
        self.dt = new_dt
        self.filtre_kalman.F[0,2] = new_dt
        self.filtre_kalman.F[1,3] = new_dt
    
    def position(self):
        #state = self.filtre_kalman.x
        #return Point(int(state[0]), int(state[1]))
        return self.last_point
    
    def vitesse(self):
        state = self.filtre_kalman.x
        return Vitesse(int(state[2]), int(state[3]))
                
    def update(self, x, y):
        if self._filtrage_acceleration(Point(x, y)):
            self.last_point = Point(x, y)
            #self.filtre_kalman.prediction()
            #self.filtre_kalman.measurement(np.array([x,y])[:, np.newaxis])
            #self.historique.append(self.position())
        #else:
            #self.last_point = None
            #self.filtre_kalman.prediction()
        
    def _filtrage_acceleration(self, pointm0):
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


class Point:
    """
    Classe permettant de définir un point mathématique dans R^2 et les opérations usuelles sur les points dans R^2
    
    :param x: abscisse
    :type x: float
    
    :param y: ordonnée
    :type y: float
    
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
        
    def __rmul__(self, other):
        return Point(self.x*other, self.y*other)
    
    def __str__(self) :
        return "("+str(self.x)+"," + str(self.y) + ")"
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def to_list(self):
        return [self.x, self.y]
        
    def unitaire(self):
        n = self.norme()
        return Point(self.x / n, self.y / n)
        
    def norme(self):
        return self.distance(Point(0, 0))
        
    def distance(self, point):
        v = self - point
        d = v.x ** 2 + v.y ** 2
        return sqrt(d)
    
    def copy(self):
        return Point(self.x, self.y)

class Vitesse:
    """
    Classe permettant de définir une vitesse sous forme de vecteur mathématique dans R^2 et les opérations usuelles sur les vecteurs dans R^2
    
    :param vx: vitesse sur x
    :type vx: float
    
    :param vy: vitesse sur y
    :type vy: float
    
    """
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy
    
    def __repr__(self):
        return '(' + str(self.vx) + ',' + str(self.vy) + ')'
        
    def __add__(self,other):
        return Vitesse(self.vx + other.vx, self.vy + other.vy)
        
    def __sub__(self,other):
        return Vitesse(self.vx - other.vx, self.vy - other.vy)
    
    def __mul__(self,other):
        return Vitesse(self.vx*other, self.vy*other)
    
    def __str__(self) :
        return "("+str(self.vx)+"," + str(self.vy) + ")"
        
    def norme(self):
        return sqrt(self.vx ** 2 + self.vy ** 2)
        
    def to_list(self):
        return [self.vx, self.vy]


def get_velocity(positions, dt):
    velocities = np.zeros(positions.shape)
    for i in range(1, velocities.shape[0]):
        velocities[i, :] = (positions[i, :] - positions[i-1, :])/float(dt)
    return velocities

if __name__ == "__main__":
    simu = Simulator(300,200)
    measures_pos = np.genfromtxt("mesures_25.txt", delimiter="\t")
    vite = get_velocity(measures_pos, 0.25)
    #print vite[:10, :]
    measures = np.concatenate((measures_pos, vite), axis=1)
    measures = np.asmatrix(measures)[:10, :]
    print measures[:10, :]
    print measures.shape
    # indice = 10
    # print measures_pos.shape
    # var = 10
    filtering = FiltrageLaserUnscented(measures[0, :].T, dt=0.25, dime=4)
    var = 1
    # #simu.add_noise_to_sensor_measures(x_reel, y_reel, var)
    for i in range(1, measures.shape[0]):
        x = measures[i, 0]
        y = measures[i, 1]
        print "x et y", x, y
        a = Convertisseur()
        #filtering.update(np.asmatrix(a.obtenir_mesures(x,y)).T)
        m1, m2, m3 = a.obtenir_mesures(x, y)
        m1, m2, m3 = m1 + np.random.randn()*var, m2 + np.random.randn()*var, m3 + np.random.randn()*var
        filtering.update(np.asmatrix([m1, m2, m3]).T)
    print "estimée", filtering.get_position_adverse_robot()
    print "vraie", measures[9, :].T