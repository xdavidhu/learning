package tk.ckdeveloper.javatitles;

import java.util.Random;

public class CharRandomizer {

	public static String randChar() {
		
		String[] letters = new String[] {
			"Q",
			"W",
			"E",
			"R",
			"T"
		};
		
		Random rand = new Random();
		
		
		return letters[rand.nextInt(letters.length)];
	}
	
}
