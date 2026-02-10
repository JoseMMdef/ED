import java.util.ArrayList;

public class MemoriaDinamica {

    public static void main(String[] args) {
        
        ArrayList<String> frutas = new ArrayList<>(); // Crear ArrayList
        
        frutas.add("Mango");
        frutas.add("Manzana");
        frutas.add("Banana");
        frutas.add("Uvas");
        
        System.out.println(frutas);
        
        frutas.remove(0);
        frutas.remove(1);
        frutas.add("sandia");
        
        System.out.println(frutas);
    }
}
