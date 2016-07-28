package balise;

import filtres.Vec2;

/**
 * Classe qui triangulaire à partir des timestamps
 * Adapté du code python de Sylvain
 * @author pf
 *
 */

public class Triangulation {

    private final static double L = 3000;
    private final static double l = 2000;
    private final static double speedOfSound = 0.34; // in mm/µs
    private final static double ecartMaxConsecutif = 6250; // µs
    private final static double ecartMaxPremierDernier = 9870; // µs
    private final static double periodeNominale = 12500; // µs
    private final static double erreurPeriode = 0.2;
    private final static double periodeMin = periodeNominale*(1-erreurPeriode); // µs
    private final static double periodeMax = periodeNominale*(1+erreurPeriode); // µs
    private static double last_t0 = 0, last_t1 = 0, last_t2 = 0; // utilisé pour vérifier la fréquence de 80Hz

    public static Vec2 computePoints(double t0, double t1, double t2)
    {
    	double t0_trie, t1_trie, t2_trie;
    	t0_trie = Math.min(t0, Math.min(t1, t2));
    	t2_trie = Math.max(t0, Math.max(t1, t2));
    	t1_trie = t0 + t1 + t2 - t0_trie - t2_trie;
    	
    	if(t1_trie - t0_trie > ecartMaxConsecutif ||t2_trie - t1_trie > ecartMaxConsecutif || t2_trie - t0_trie > ecartMaxPremierDernier)
    	{
    		System.err.println("Triplet incohérent");
    		return null;
    	}
    	
    	if(last_t0 != 0 &&
    			(t0 - last_t0 < periodeMin || t0 - last_t0 > periodeMax
    			|| t1 - last_t1 < periodeMin || t1 - last_t1 > periodeMax
    			|| t2 - last_t2 < periodeMin || t2 - last_t2 > periodeMax))
    	{
    		System.err.println("Erreur de fréquence ! "+(1000000 / (t0 - last_t0) + 1000000 / (t1 - last_t1) + 1000000 / (t2 - last_t2)) / 3);
    	}
//		System.err.println("Fréquence : "+1000000 / ((t0 - last_t0)));

    	
    	last_t0 = t0;
    	last_t1 = t1;
    	last_t2 = t2;
    		
    	double k1 = (t2 - t1) * speedOfSound;
    	double k2 = (t2 - t0) * speedOfSound;
    	double k3 = (t1 - t0) * speedOfSound;
    	
        double cte = -(-2*k2+k3)*(-2*k2+k3)*l*l*(k3*k3-l*l)*(4*k2*k2-l*l-4*L*L)*(4*k2*k2-8*k2*k3+4*k3*k3-l*l-4*L*L);
        double sq;
        if(cte >= 0)
            sq = Math.sqrt(cte);
        else
        {
            System.err.println("cte = " + cte + ", k2 = " + k2 + ", k3 = " + k3);
            return null;
        }

        double ax = -8*k2*k2*k3*k3*L+8*k2*k3*k3*k3*L-4*k3*k3*l*l*L+2*l*l*l*l*L;
        double bx = sq;
        double cx = 4*(4*k2*k2*l*l-4*k2*k3*l*l+k3*k3*l*l+4*k3*k3*L*L-4*l*l*L*L);

        double ay = 16*k2*k2*k2*k2*k3*l*l-32*k2*k2*k2*k3*k3*l*l+20*k2*k2*k3*k3*k3*l*l-4*k2*k3*k3*k3*k3*l*l+16*k2*k2*k2*l*l*l*l-20*k2*k2*k3*l*l*l*l+8*k2*k3*k3*l*l*l*l-k3*k3*k3*l*l*l*l-16*k2*k2*k3*l*l*L*L+32*k2*k3*k3*l*l*L*L-12*k3*k3*k3*l*l*L*L-16*k2*l*l*l*l*L*L+8*k3*l*l*l*l*L*L;
        double by = 2*k3*L*sq;
        double cy = 4*(2*k2-k3)*l*(4*k2*k2*l*l-4*k2*k3*l*l+k3*k3*l*l+4*k3*k3*L*L-4*l*l*L*L);

//        System.out.println("sq = "+sq+", ax = "+ax+", bx = "+bx+", cx = "+cx+", ay = "+ay+", by = "+by+", cy = "+cy);
        
        double X1 = (ax + bx) / cx;
        double Y1 = (ay + by) / cy;
        double X2 = (ax - bx) / cx;
        double Y2 = (ay - by) / cy;

        Vec2 point1 = new Vec2((int)(X1), (int)(Y1));
        Vec2 point2 = new Vec2((int)(X2), (int)(Y2));
        
        double[] temps = new double[3];
        
		temps[0] = (point1.distance(new Vec2(-1500, 0)));
		temps[1] = (point1.distance(new Vec2(-1500, 2000)));
		temps[2] = (point1.distance(new Vec2(1500, 1000)));

		if((Math.abs(temps[2] - temps[1] - k1) > 20) || (Math.abs(temps[2] - temps[0] - k2) > 20) || (Math.abs(temps[1] - temps[0] - k3) > 20))
		{
//			System.out.println("Autre solution : "+point1);
			return point2;
		}
        
//		System.out.println("Autre solution : "+point2);
        return point1;
//        System.out.println(point1+" "+point2);

    }
    
}
