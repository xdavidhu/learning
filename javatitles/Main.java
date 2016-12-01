package tk.ckdeveloper.javatitles;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.Charset;
import java.util.Scanner;

public class Main {
	
	static String hp = "O O O";
	static int point = 0;
	static int lvl = 1;

	@SuppressWarnings("static-access")
	public static void main(String[] args) throws Exception {
		
		Scanner s = new Scanner(System.in);
		
		//INTRO
		
		System.out.println("     _                 _____ _ _   _           ");
		System.out.println("    | | __ ___   ____ |_   _(_) |_| | ___  ___ ");
		System.out.println(" _  | |/ _` \\ \\ / / _` || | | | __| |/ _ \\/ __|");
		System.out.println("| |_| | (_| |\\ V / (_| || | | | |_| |  __/\\__ \\");
		System.out.println(" \\___/ \\__,_| \\_/ \\__,_||_| |_|\\__|_|\\___||___/");
		
		System.out.println("Version: 1.6.2 | @xdavidhu");
		
		Sleep.sleep(300);
		System.out.println(" ");
		System.out.print("Loading");
		Sleep.sleep(250);
		System.out.print(".");
		Sleep.sleep(250);
		System.out.print(".");
		Sleep.sleep(250);
		System.out.print(".");
		Sleep.sleep(250);
		System.out.println("");
		System.out.println("");
		System.out.println("Type the letters as fast as you can.");
		System.out.println("You have 3 HP. It looks like this: O O O");
		System.out.println("");
		System.out.println("Time you have:");
		System.out.println("Lvl 1 - 2,0 Sec");
		System.out.println("Lvl 2 - 1,6 Sec");
		System.out.println("Lvl 3 - 1,4 Sec");
		System.out.println("Lvl 4 - 1,2 Sec");
		System.out.println("Lvl 5 - 1,0 Sec");
		System.out.println("Lvl 6 - 0,9 Sec");
		System.out.println("");
		System.out.println("Press enter to start.");
		s.nextLine();
		
		String task;
		long time;
		
		int round = 0;
		
		//Levels
		int[] lvlTime = new int[]{
			0, //LVL 0
			2000,
			1600,
			1400,
			1200,
			1000,
			900
		};
		
		
		while (true) {
			
		round++;
		
		if (round == 10){
			lvl++;
			imgGenerator.lvlUpImg(lvl);
			Sleep.sleep(1000);
		}
		else if (round == 20){
			lvl++;
			imgGenerator.lvlUpImg(lvl);
			Sleep.sleep(900);
		}
		else if (round == 35){
			lvl++;
			imgGenerator.lvlUpImg(lvl);
			Sleep.sleep(800);
		}
		else if (round == 60){
			lvl++;
			imgGenerator.lvlUpImg(lvl);
			Sleep.sleep(700);
		}
		else if (round == 80){
			lvl++;
			imgGenerator.lvlUpImg(lvl);
			Sleep.sleep(700);
		}
			
			
		task = CharRandomizer.randChar();
		
		imgGenerator.newImg(point, hp, task, lvl);
		
		String input;
		
		
		//Timer
		
		Stopwatch timer = new Stopwatch();
		
		timer.start();
		
		input = s.nextLine();
		
		timer.stop();
		time = timer.getElapsedTime();
		
		//Q
		
//		System.out.println(time);
//		System.out.println(lvlTime[lvl]);
		
		if (time < lvlTime[lvl]) {
		
		if (task.equalsIgnoreCase("Q")){
			
			if (input.equalsIgnoreCase("q")) {
				point++;
//				System.out.println("Correct! Q");
			}
			else {
//				System.out.println("Not correct! Q");
				if (!setHealth()) {
					break;
				}
			}
		
		}
			
		//W
		
		else if (task.equalsIgnoreCase("W")){
			if (input.equalsIgnoreCase("w")) {
				point++;
//				System.out.println("Correct! W");
			}
			else {
//				System.out.println("Not correct! W");
				if (!setHealth()) {
					break;
				}
			}
		}
		
		
		//E
		
		else if (task.equalsIgnoreCase("E")){
			if (input.equalsIgnoreCase("e")) {
				point++;
//				System.out.println("Correct! E");
			}
			else {
//				System.out.println("Not correct! E");
				if (!setHealth()) {
					break;
				}
			}
		}
		
		
		//R
		
		else if (task.equalsIgnoreCase("R")){
			if (input.equalsIgnoreCase("r")) {
				point++;
//				System.out.println("Correct! R");
			}
			else {
				if (!setHealth()) {
//					System.out.println("Not correct! R");
					break;
				}
			}
		}
		
		
		//T
		
		else if (task.equalsIgnoreCase("T")) {
			if (input.equalsIgnoreCase("t")) {
				point++;
//				System.out.println("Correct! T");
			}
			else {
//				System.out.println("Not correct! T");
				if (!setHealth()) {
					break;
				}
			}
		}
		
		}
		//if time is over
		else {
//			System.out.println("Not correct! TIME");
			if (!setHealth()) {
				break;
			}
		}

	}
		
		String newGame;

		String postArgs;
		postArgs = "point=" + point + "&level=" + lvl;
		PostAPI.postToPage("http", "46.101.229.103", "/api/", "javatitleslog", postArgs);
		
		System.out.println("");
		System.out.println("New game? (Y/n)");
		
		newGame = s.nextLine();
		
		if (newGame.equalsIgnoreCase("Y")) {
			System.out.println("'NEW GAME' selected.");
			
			//resetting values
			point = 0;
			hp = "O O O";
			round = 0;
			lvl = 1;
			
			new Main().main(null);
		}
		else {
			System.out.println("'EXIT GAME' selected.");
			System.out.print("Exiting");
			Sleep.sleep(250);
			System.out.print(".");
			Sleep.sleep(250);
			System.out.print(".");
			Sleep.sleep(250);
			System.out.print(".");
			Sleep.sleep(250);
			System.out.println("");
			s.close();
			Clear.clearLines(50);
			System.exit(0);
		}
			
	}
	
	public static boolean setHealth(){
		
		if (hp.equalsIgnoreCase("O O O")) {
			hp = "O O X";
			imgGenerator.damage(hp);
			return true;
		}
		else if (hp.equalsIgnoreCase("O O X")) {
			hp = "O X X";
			imgGenerator.damage(hp);
			return true;
		}
		else {
			imgGenerator.damage("X X X");
			Clear.clearLines(24);
			System.out.println("Game over! - No more HP!");
			System.out.println("");
			System.out.println("Yor points: " + point);
			System.out.println("Your level: " + lvl);
			Sleep.sleep(500);
			return false;
		}
	
	}

}
