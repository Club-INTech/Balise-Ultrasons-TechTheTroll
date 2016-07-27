package filtres;

/**
 * Interface pour tous les filtres
 * @author pf
 *
 */

public interface Filtre
{
	/**
	 * Initialise en utilisant pas d'échantillonnage
	 * @param deltaTemps
	 */
	public void init(double deltaTemps);
	
	/**
	 * Filtre un point donné en entrée (les données brutes sont aussi disponibles)
	 * @param t1
	 * @param t2
	 * @param t3
	 * @param positionBrute
	 * @return
	 */
	public Vec2 filtre(double t1, double t2, double t3, Vec2 positionBrute);
	
}
