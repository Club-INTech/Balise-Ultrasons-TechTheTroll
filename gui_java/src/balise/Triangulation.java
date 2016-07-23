package balise;

/**
 * Classe qui triangulaire à partir des timestamps
 * Adapté du code python de Sylvain
 * @author pf
 *
 */

public class Triangulation {

    private final static int L = 3000;
    private final static int l = 2000;
    private final static double speedOfSound = 0.34; // in mm/µs

    private static Point point1;
    private static Point point2;
    
    public static Point getPoint1()
    {
    	return point1;
    }

    public static Point getPoint2()
    {
    	return point2;
    }

    public static void computePoints(double t0, double t1, double t2)
    {
    	double k2 = (t2 - t0) * speedOfSound;
    	double k3 = (t1 - t0) * speedOfSound;

        double cte = -Math.pow(-2*k2+k3,2)*l*l*(k3*k3-l*l)*(4*k2*k2-l*l-4*L*L)*(4*k2*k2-8*k2*k3+4*k3*k3-l*l-4*L*L);
        double sq;
        if(cte >= 0)
            sq = Math.sqrt(cte);
        else
        {
            System.err.println("cte = " + cte + ", k2 = " + k2 + ", k3 = " + k3);
            return;
        }

        double ax = -8*k2*k2*k3*k3*L+8*k2*k3*k3*k3*L-4*k3*k3*l*l*L+2*l*l*l*l*L;
        double bx = sq;
        double cx = 4*(4*k2*k2*l*l-4*k2*k3*l*l+k3*k3*l*l+4*k3*k3*L*L-4*l*l*L*L);

        double ay = 16*k2*k2*k2*k2*k3*l*l-32*k2*k2*k2*k3*k3*l*l+20*k2*k2*k3*k3*k3*l*l-4*k2*k3*k3*k3*k3*l*l+16*k2*k2*k2*l*l*l*l-20*k2*k2*k3*l*l*l*l+8*k2*k3*k3*l*l*l*l-k3*k3*k3*l*l*l*l-16*k2*k2*k3*l*l*L*L+32*k2*k3*k3*l*l*L*L-12*k3*k3*k3*l*l*L*L-16*k2*l*l*l*l*L*L+8*k3*l*l*l*l*L*L;
        double by = 2*k3*L*sq;
        double cy = 4*(2*k2-k3)*l*(4*k2*k2*l*l-4*k2*k3*l*l+k3*k3*l*l+4*k3*k3*L*L-4*l*l*L*L);

        double X1 = (ax + bx) / cx;
        double Y1 = (ay + by) / cy + 1000;
        double X2 = (ax - bx) / cx;
        double Y2 = (ay - by) / cy + 1000;

        point1 = new Point((int)(X1), (int)(Y1), Couleur.ROUGE);
        point2 = new Point((int)(X2), (int)(Y2), Couleur.BLEU);
        
        System.out.println(point1+" "+point2);

    }
    
}
