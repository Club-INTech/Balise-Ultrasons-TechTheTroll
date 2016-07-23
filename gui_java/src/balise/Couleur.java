package balise;

import java.awt.Color;

/**
 * Définition de quelques couleurs
 * @author pf
 *
 */
public enum Couleur {
	BLANC(new Color(255, 255, 255, 0)),
	NOIR(new Color(0, 0, 0, 255)),
	BLEU(new Color(0, 0, 200, 255)),
	JAUNE(new Color(200, 200, 0, 255)),
	ROUGE(new Color(200, 0, 0, 255)),
	VIOLET(new Color(200, 0, 200, 255));
	
	public final Color couleur;
	
	private Couleur(Color couleur)
	{
		this.couleur = couleur;
	}
}
