package learning.devops;

public final class App {
    private App() {
    }

    public static String message() {
        return "Gradle DevOps application is running";
    }

    public static void main(String[] args) {
        System.out.println(message());
    }
}
