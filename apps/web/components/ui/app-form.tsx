import {
    Field,
    FieldDescription,
    FieldGroup,
    FieldLabel,
    FieldSet,
  } from "@/components/ui/field"
  import { Input } from "@/components/ui/input"
  import { Button } from "@/components/ui/button"
  import { useState } from "react"

  export function AppForm() {

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        console.log("Form submitted")
        console.log(name, lastName)
    }

    let name: string = ""
    let lastName: string = ""

    return (
        <FieldSet>
            <FieldGroup>
                <Field><FieldLabel>First Name</FieldLabel>
                    <Input type="text" name="John" />
                    <FieldDescription>This is the first name</FieldDescription>
                </Field>

                <Field>
                    <FieldLabel>Last Name</FieldLabel>
                    <Input type="text" lastName="Smith" />
                <FieldDescription>This is the last name</FieldDescription>
                </Field>
                
                <Field orientation="responsive">
                    <Button type="button" onClick={handleSubmit(name, lastName)}>Reset</Button>

                </Field>
            </ FieldGroup>
        </FieldSet>
    )
}