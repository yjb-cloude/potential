public class zoo {
    public static void main(String[] args) {

        Animal[] animal = new Animal[3];
        animal[0] = new Dog("旺财");
        animal[1] = new Cat("mimi");
        animal[2] = new Dog("小黄");
        for (Animal a : animal) {
            a.speak();
        }
    }
}
