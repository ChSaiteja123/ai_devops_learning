package learning.devops;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class AppTest {
    @Test
    void returnsApplicationMessage() {
        assertEquals("Gradle DevOps application is running", App.message());
    }
}
