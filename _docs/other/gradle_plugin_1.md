# Chapter 41. Writing Custom Plugins

Table of Contents

- [41.1. Packaging a plugin](https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:packaging_a_plugin)
- [41.2. Writing a simple plugin](https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:writing_a_simple_plugin)
- [41.3. Getting input from the build](https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:getting_input_from_the_build)
- [41.4. Working with files in custom tasks and plugins](https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:working_with_files_in_custom_tasks_and_plugins)
- [41.5. Mapping extension properties to task properties](https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:mapping_extension_properties_to_task_properties)
- [41.6. A standalone project](https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:custom_plugins_standalone_project)
- [41.7. Maintaining multiple domain objects](https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:maintaining_multiple_domain_objects)

A Gradle plugin packages up reusable pieces of build logic, which can be used across many different projects and builds. Gradle allows you to implement your own custom plugins, so you can reuse your build logic, and share it with others.

You can implement a custom plugin in any language you like, provided the implementation ends up compiled as bytecode. For the examples here, we are going to use Groovy as the implementation language. You could use Java or Scala instead, if you want.

## 41.1. Packaging a plugin

There are several places where you can put the source for the plugin.

- Build script

  You can include the source for the plugin directly in the build script. This has the benefit that the plugin is automatically compiled and included in the classpath of the build script without you having to do anything. However, the plugin is not visible outside the build script, and so you cannot reuse the plugin outside the build script it is defined in.

- `buildSrc` project

  You can put the source for the plugin in the `*rootProjectDir*/buildSrc/src/main/groovy` directory. Gradle will take care of compiling and testing the plugin and making it available on the classpath of the build script. The plugin is visible to every build script used by the build. However, it is not visible outside the build, and so you cannot reuse the plugin outside the build it is defined in.See [Chapter 43, *Organizing Build Logic*](https://docs.gradle.org/4.1/userguide/organizing_build_logic.html) for more details about the `buildSrc` project.

- Standalone project

  You can create a separate project for your plugin. This project produces and publishes a JAR which you can then use in multiple builds and share with others. Generally, this JAR might include some custom plugins, or bundle several related task classes into a single library. Or some combination of the two.

In our examples, we will start with the plugin in the build script, to keep things simple. Then we will look at creating a standalone project.

## 41.2. Writing a simple plugin

To create a custom plugin, you need to write an implementation of [`Plugin`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/Plugin.html). Gradle instantiates the plugin and calls the plugin instance's [`Plugin.apply(T)`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/Plugin.html#apply(T)) method when the plugin is used with a project. The project object is passed as a parameter, which the plugin can use to configure the project however it needs to. The following sample contains a greeting plugin, which adds a `hello` task to the project.



**Example 41.1. A custom plugin**

```
build.gradle
apply plugin: GreetingPlugin

class GreetingPlugin implements Plugin<Project> {
    void apply(Project project) {
        project.task('hello') {
            doLast {
                println "Hello from the GreetingPlugin"
            }
        }
    }
}
```

Output of **gradle -q hello**

```
> gradle -q hello
Hello from the GreetingPlugin
```

One thing to note is that a new instance of a given plugin is created for each project it is applied to. Also note that the [`Plugin`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/Plugin.html) class is a generic type. This example has it receiving the [`Project`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html) type as a type parameter. It's possible to write unusual custom plugins that take different type parameters, but this will be unlikely (until someone figures out more creative things to do here).

## 41.3. Getting input from the build

Most plugins need to obtain some configuration from the build script. One method for doing this is to use *extension objects*. The Gradle [`Project`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html) has an associated [`ExtensionContainer`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/plugins/ExtensionContainer.html) object that helps keep track of all the settings and properties being passed to plugins. You can capture user input by telling the extension container about your plugin. To capture input, simply add a Java Bean compliant class into the extension container's list of extensions. Groovy is a good language choice for a plugin because plain old Groovy objects contain all the getter and setter methods that a Java Bean requires.

Let's add a simple extension object to the project. Here we add a `greeting` extension object to the project, which allows you to configure the greeting.



**Example 41.2. A custom plugin extension**

```
build.gradle
apply plugin: GreetingPlugin

greeting.message = 'Hi from Gradle'

class GreetingPlugin implements Plugin<Project> {
    void apply(Project project) {
        // Add the 'greeting' extension object
        project.extensions.create("greeting", GreetingPluginExtension)
        // Add a task that uses the configuration
        project.task('hello') {
            doLast {
                println project.greeting.message
            }
        }
    }
}

class GreetingPluginExtension {
    def String message = 'Hello from GreetingPlugin'
}
```

Output of **gradle -q hello**

```
> gradle -q hello
Hi from Gradle
```

In this example, `GreetingPluginExtension` is a plain old Groovy object with a field called `message`. The extension object is added to the plugin list with the name `greeting`. This object then becomes available as a project property with the same name as the extension object.

Oftentimes, you have several related properties you need to specify on a single plugin. Gradle adds a configuration closure block for each extension object, so you can group settings together. The following example shows you how this works.



**Example 41.3. A custom plugin with configuration closure**

```
build.gradle
apply plugin: GreetingPlugin

greeting {
    message = 'Hi'
    greeter = 'Gradle'
}

class GreetingPlugin implements Plugin<Project> {
    void apply(Project project) {
        project.extensions.create("greeting", GreetingPluginExtension)
        project.task('hello') {
            doLast {
                println "${project.greeting.message} from ${project.greeting.greeter}"
            }
        }
    }
}

class GreetingPluginExtension {
    String message
    String greeter
}
```

Output of **gradle -q hello**

```
> gradle -q hello
Hi from Gradle
```

In this example, several settings can be grouped together within the `greeting` closure. The name of the closure block in the build script (`greeting`) needs to match the extension object name. Then, when the closure is executed, the fields on the extension object will be mapped to the variables within the closure based on the standard Groovy closure delegate feature.

## 41.4. Working with files in custom tasks and plugins

When developing custom tasks and plugins, it's a good idea to be very flexible when accepting input configuration for file locations. To do this, you can leverage the [`Project.file(java.lang.Object)`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html#org.gradle.api.Project:file(java.lang.Object)) method to resolve values to files as late as possible.



**Example 41.4. Evaluating file properties lazily**

```
build.gradle
class GreetingToFileTask extends DefaultTask {

    def destination

    File getDestination() {
        project.file(destination)
    }

    @TaskAction
    def greet() {
        def file = getDestination()
        file.parentFile.mkdirs()
        file.write "Hello!"
    }
}

task greet(type: GreetingToFileTask) {
    destination = { project.greetingFile }
}

task sayGreeting(dependsOn: greet) {
    doLast {
        println file(greetingFile).text
    }
}

ext.greetingFile = "$buildDir/hello.txt"
```

Output of **gradle -q sayGreeting**

```
> gradle -q sayGreeting
Hello!
```

In this example, we configure the `greet` task `destination` property as a closure, which is evaluated with the [`Project.file(java.lang.Object)`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html#org.gradle.api.Project:file(java.lang.Object)) method to turn the return value of the closure into a file object at the last minute. You will notice that in the example above we specify the `greetingFile` property value after we have configured to use it for the task. This kind of lazy evaluation is a key benefit of accepting any value when setting a file property, then resolving that value when reading the property.

## 41.5. Mapping extension properties to task properties

Capturing user input from the build script through an extension and mapping it to input/output properties of a custom task is considered a best practice. The end user only interacts with the exposed DSL defined by the extension. The imperative logic is hidden in the plugin implementation.

The extension declaration in the build script as well as the mapping between extension properties and custom task properties occurs during Gradle's configuration phase of the build lifecycle. To avoid evaluation order issues, the actual value of a mapped property has to be resolved during the execution phase. For more information please see [Section 22.1, “Build phases”](https://docs.gradle.org/4.1/userguide/build_lifecycle.html#sec:build_phases). Gradle's API offers the mutable type [`PropertyState`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/PropertyState.html) for representing a property that should be lazily evaluated e.g. during execution time. The method [`PropertyState.set(T)`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/PropertyState.html#set(T)) provides the value, [`Provider.get()`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/Provider.html#get()) returns the value upon request.

The following demonstrates the usage of the type for mapping an extension property to a task property:



**Example 41.5. Mapping extension properties to task properties**

```
build.gradle
apply plugin: GreetingPlugin

greeting {
    message = 'Hi from Gradle'
    outputFiles = files('a.txt', 'b.txt')
}

class GreetingPlugin implements Plugin<Project> {
    void apply(Project project) {
        // Add the 'greeting' extension object
        def extension = project.extensions.create('greeting', GreetingPluginExtension, project)
        // Add a task that uses the configuration
        project.tasks.create('hello', Greeting) {
            message = extension.messageProvider
            outputFiles = extension.outputFiles
        }
    }
}

class GreetingPluginExtension {
    final PropertyState<String> message
    final ConfigurableFileCollection outputFiles

    GreetingPluginExtension(Project project) {
        message = project.property(String)
        setMessage('Hello from GreetingPlugin')
        outputFiles = project.files()
    }

    String getMessage() {
        message.get()
    }

    Provider<String> getMessageProvider() {
        message
    }

    void setMessage(String message) {
        this.message.set(message)
    }

    FileCollection getOutputFiles() {
        outputFiles
    }

    void setOutputFiles(FileCollection outputFiles) {
        this.outputFiles.setFrom(outputFiles)
    }
}

class Greeting extends DefaultTask {
    final PropertyState<String> message = project.property(String)
    final ConfigurableFileCollection outputFiles = project.files()

    @Input
    String getMessage() {
        message.get()
    }

    void setMessage(String message) {
        this.message.set(message)
    }

    void setMessage(Provider<String> message) {
        this.message.set(message)
    }

    FileCollection getOutputFiles() {
        outputFiles
    }

    void setOutputFiles(FileCollection outputFiles) {
        this.outputFiles.setFrom(outputFiles)
    }

    @TaskAction
    void printMessage() {
        getOutputFiles().each {
            logger.quiet "Writing message 'Hi from Gradle' to file"
            it.text = getMessage()
        }
    }
}
```

*Note:* The code for this example can be found at `samples/userguide/tasks/mapExtensionPropertiesToTaskProperties` in the ‘-all’ distribution of Gradle.

Output of **gradle -q hello**

```
> gradle -q hello
Writing message 'Hi from Gradle' to file
Writing message 'Hi from Gradle' to file
```

The example above uses instances of [`Provider`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/Provider.html) and [`PropertyState`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/PropertyState.html). The main difference between these two interfaces is attributed to mutability. A [`Provider`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/Provider.html) is immutable and can be created with the method [`Project.provider(java.util.concurrent.Callable)`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/Project.html#provider(java.util.concurrent.Callable)). [`PropertyState`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/PropertyState.html) extends the interface [`Provider`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/provider/Provider.html), represents a mutable value and can be created with the method [`Project.property(java.lang.Class)`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html#org.gradle.api.Project:property(java.lang.Class)). Please note that the provider types are not intended for for implementation by build script or plugin authors.

The [`Project`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html) does not provide a specific method signature for creating a provider by passing in a `groovy.lang.Closure` as parameter. When writing a plugin implementation with Groovy, you can use the method signature accepting a `java.util.concurrent.Callable` parameter. Groovy's [Closure to type coercion](http://docs.groovy-lang.org/next/html/documentation/core-semantics.html#_assigning_a_closure_to_a_sam_type) will take of the rest.

## 41.6. A standalone project

Now we will move our plugin to a standalone project, so we can publish it and share it with others. This project is simply a Groovy project that produces a JAR containing the plugin classes. Here is a simple build script for the project. It applies the Groovy plugin, and adds the Gradle API as a compile-time dependency.



**Example 41.6. A build for a custom plugin**

```
build.gradle
apply plugin: 'groovy'

dependencies {
    compile gradleApi()
    compile localGroovy()
}
```

*Note:* The code for this example can be found at `samples/customPlugin/plugin` in the ‘-all’ distribution of Gradle.

So how does Gradle find the [`Plugin`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/Plugin.html) implementation? The answer is you need to provide a properties file in the jar's `META-INF/gradle-plugins` directory that matches the id of your plugin.



**Example 41.7. Wiring for a custom plugin**

```
src/main/resources/META-INF/gradle-plugins/org.samples.greeting.properties
implementation-class=org.gradle.GreetingPlugin
```

Notice that the properties filename matches the plugin id and is placed in the resources folder, and that the `implementation-class` property identifies the [`Plugin`](https://docs.gradle.org/4.1/javadoc/org/gradle/api/Plugin.html) implementation class.

### 41.6.1. Creating a plugin id

Plugin ids are fully qualified in a manner similar to Java packages (i.e. a reverse domain name). This helps to avoid collisions and provides a way to group plugins with similar ownership.

Your plugin id should be a combination of components that reflect namespace (a reasonable pointer to you or your organization) and the name of the plugin it provides. For example if you had a Github account named “foo” and your plugin was named “bar”, a suitable plugin id might be `com.github.foo.bar`. Similarly, if the plugin was developed at the baz organization, the plugin id might be `org.baz.bar`.

Plugin ids should conform to the following:

- May contain any alphanumeric character, '.', and '-'.
- Must contain at least one '.' character separating the namespace from the name of the plugin.
- Conventionally use a lowercase reverse domain name convention for the namespace.
- Conventionally use only lowercase characters in the name.
- `org.gradle` and `com.gradleware` namespaces may not be used.
- Cannot start or end with a '.' character.
- Cannot contain consecutive '.' characters (i.e. '..').

Although there are conventional similarities between plugin ids and package names, package names are generally more detailed than is necessary for a plugin id. For instance, it might seem reasonable to add “gradle” as a component of your plugin id, but since plugin ids are only used for Gradle plugins, this would be superfluous. Generally, a namespace that identifies ownership and a name are all that are needed for a good plugin id.

### 41.6.2. Publishing your plugin

If you are publishing your plugin internally for use within your organization, you can publish it like any other code artifact. See the [ivy](https://docs.gradle.org/4.1/userguide/publishing_ivy.html) and [maven](https://docs.gradle.org/4.1/userguide/publishing_maven.html) chapters on publishing artifacts.

If you are interested in publishing your plugin to be used by the wider Gradle community, you can publish it to the [Gradle plugin portal](http://plugins.gradle.org/). This site provides the ability to search for and gather information about plugins contributed by the Gradle community. See the instructions [here](http://plugins.gradle.org/docs/submit) on how to make your plugin available on this site.

### 41.6.3. Using your plugin in another project

To use a plugin in a build script, you need to add the plugin classes to the build script's classpath. To do this, you use a “`buildscript { }`” block, as described in [the section called “Applying plugins with the buildscript block”](https://docs.gradle.org/4.1/userguide/plugins.html#sec:applying_plugins_buildscript). The following example shows how you might do this when the JAR containing the plugin has been published to a local repository:



**Example 41.8. Using a custom plugin in another project**

```
build.gradle
buildscript {
    repositories {
        maven {
            url uri('../repo')
        }
    }
    dependencies {
        classpath group: 'org.gradle', name: 'customPlugin',
                  version: '1.0-SNAPSHOT'
    }
}
apply plugin: 'org.samples.greeting'
```

Alternatively, if your plugin is published to the plugin portal, you can use the incubating plugins DSL (see [Section 27.5.2, “Applying plugins with the plugins DSL”](https://docs.gradle.org/4.1/userguide/plugins.html#sec:plugins_block)) to apply the plugin:



**Example 41.9. Applying a community plugin with the plugins DSL**

```
build.gradle
plugins {
    id "com.jfrog.bintray" version "0.4.1"
}
```

### 41.6.4. Writing tests for your plugin

You can use the [`ProjectBuilder`](https://docs.gradle.org/4.1/javadoc/org/gradle/testfixtures/ProjectBuilder.html) class to create [`Project`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html) instances to use when you test your plugin implementation.



**Example 41.10. Testing a custom plugin**

```
src/test/groovy/org/gradle/GreetingPluginTest.groovy
class GreetingPluginTest {
    @Test
    public void greeterPluginAddsGreetingTaskToProject() {
        Project project = ProjectBuilder.builder().build()
        project.pluginManager.apply 'org.samples.greeting'

        assertTrue(project.tasks.hello instanceof GreetingTask)
    }
}
```

### 41.6.5. Using the Java Gradle Plugin development plugin

You can use the incubating [Java Gradle Plugin development plugin](https://docs.gradle.org/4.1/userguide/javaGradle_plugin.html) to eliminate some of the boilerplate declarations in your build script and provide some basic validations of plugin metadata. This plugin will automatically apply the [Java plugin](https://docs.gradle.org/4.1/userguide/java_plugin.html), add the `gradleApi()` dependency to the compile configuration, and perform plugin metadata validations as part of the `jar` task execution.



**Example 41.11. Using the Java Gradle Plugin Development plugin**

```
build.gradle
plugins {
    id "java-gradle-plugin"
}
```

When publishing plugins to custom plugin repositories using the [ivy](https://docs.gradle.org/4.1/userguide/publishing_ivy.html) or [maven](https://docs.gradle.org/4.1/userguide/publishing_maven.html) publish plugins, the [Java Gradle Plugin development plugin](https://docs.gradle.org/4.1/userguide/javaGradle_plugin.html) will also generate plugin marker artifacts named based on the plugin id which depend on the plugin's implementation artifact.

## 41.7. Maintaining multiple domain objects

Gradle provides some utility classes for maintaining collections of objects, which work well with the Gradle build language.



**Example 41.12. Managing domain objects**

```
build.gradle
apply plugin: DocumentationPlugin

books {
    quickStart {
        sourceFile = file('src/docs/quick-start')
    }
    userGuide {

    }
    developerGuide {

    }
}

task books {
    doLast {
        books.each { book ->
            println "$book.name -> $book.sourceFile"
        }
    }
}

class DocumentationPlugin implements Plugin<Project> {
    void apply(Project project) {
        def books = project.container(Book)
        books.all {
            sourceFile = project.file("src/docs/$name")
        }
        project.extensions.books = books
    }
}

class Book {
    final String name
    File sourceFile

    Book(String name) {
        this.name = name
    }
}
```

Output of **gradle -q books**

```
> gradle -q books
developerGuide -> /home/user/gradle/samples/userguide/organizeBuildLogic/customPluginWithDomainObjectContainer/src/docs/developerGuide
quickStart -> /home/user/gradle/samples/userguide/organizeBuildLogic/customPluginWithDomainObjectContainer/src/docs/quick-start
userGuide -> /home/user/gradle/samples/userguide/organizeBuildLogic/customPluginWithDomainObjectContainer/src/docs/userGuide
```

The [`Project.container(java.lang.Class)`](https://docs.gradle.org/4.1/dsl/org.gradle.api.Project.html#org.gradle.api.Project:container(java.lang.Class)) methods create instances of [`NamedDomainObjectContainer`](https://docs.gradle.org/4.1/dsl/org.gradle.api.NamedDomainObjectContainer.html), that have many useful methods for managing and configuring the objects. In order to use a type with any of the `project.container` methods, it MUST expose a property named “`name`” as the unique, and constant, name for the object. The `project.container(Class)` variant of the container method creates new instances by attempting to invoke the constructor of the class that takes a single string argument, which is the desired name of the object. See the above link for `project.container` method variants that allow custom instantiation strategies.



https://docs.gradle.org/4.1/userguide/custom_plugins.html#sec:custom_plugins_standalone_project

