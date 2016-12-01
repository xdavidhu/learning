package tk.ckdeveloper.javatitles;

public class imgGenerator {

	public static void newImg(int p, String hp, String t, int l) {
		
		System.out.println("\n\n\n\n\n\n\n\n\n");
		System.out.println("Points: " + p);
		System.out.println("Health: " + hp);
		System.out.println("Level: " + l);
		System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n");
		BigLetters.bigletter(t);
		
	}
	
	public static void lvlUpImg(int l) {
		
		System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
		System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
		
		System.out.println("                                  LEVEL UP!");
		System.out.println("");
		System.out.println("                                New level: " + l + "!");
		System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
		
	}
	
	public static void damage(String s) {
		
		if (s.equalsIgnoreCase("O O X")){
			
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n");
			
			BigLetters.bigletter("hearth3");
			
			System.out.println("");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			Sleep.sleep(500);
			
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			BigLetters.bigletter("hearth2");
			
			System.out.println("");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			Sleep.sleep(500);
			
		}
		else if (s.equalsIgnoreCase("O X X")){
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n");
			
			BigLetters.bigletter("hearth2");
			
			System.out.println("");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			Sleep.sleep(500);
			
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			BigLetters.bigletter("hearth1");
			
			System.out.println("");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			Sleep.sleep(500);
		}
		else {
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n");
			
			BigLetters.bigletter("hearth1");
			
			System.out.println("");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			Sleep.sleep(500);
			
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			BigLetters.bigletter("hearth0");
			
			System.out.println("");
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n");
			
			Sleep.sleep(500);
		}
		
	}
	
	
}
