#include <iostream>

/// Class for Animal
class animal
{
public:
    animal(char *name, int age) :
            name_(name),
            age_(age)
    {}

    ~animal()
    {}

    void introduce()
    {
        std::cout << " Hello I am " << name_ << " and I am " << age_ << " years old." << std::endl;
    }

private:
    char *name_;
    int age_;
};

int main() {
    animal dog("kral", 7);
    dog.introduce();

    return 0;
}
